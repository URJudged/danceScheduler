## \file dance_scheduler.py
#  \author Judge Lee (jblee@hmc.edu)
#  \date June 4, 2016
#  
#  Source file for a scheduler meant to simplify performance scheduling weighted by performer rest
#  and reducing the number of consecutive low energy performances.

import sys
import math
import random
import functools


## \class Performer
#  \brief Stores information for a performer
class Performer:
	'Stores information for a performer'

	## 
	#  \param[in] name      The name of the performer as a string
	#  \param[in] routines  A list of Routines the performer is in
	def __init__(self, name = '', routines = []):
		self.name = name
		self.routines = routines
		for rout in self.routines:
			rout.performers.append(self)
			rout.performers = list(set(rout.performers))

	## 
	#  \brief  Formats a performer as a string. Example:
	#  \code
	#  Bo Lee
	#    Routines:
	#     * 0: Dance 0
	#     * 4: Dance 4
	#    Score: 4
	#  \endcode
	def __repr__(self):
		output =  self.name + '\n'
		output += '  Routines: \n'
		for rout in self.routines:
			output += '   ' + str(rout.order) + ": " + rout.name + '\n'
		output += '  Score: ' + str(self.score()) + '\n'
		return output

	def __contains__(self, rout):
		return rout in self.routines

	def __lt__(self, other):
		return self.score() < other.score()

	def __le__(self, other):
		return self.score() <= other.score()

	def __gt__(self, other):
		return self.score() > other.score()

	def __ge__(self, other):
		return self.score() >= other.score()

	def score(self):
		return len(self.routines) * len(self.routines)


## \class Routine
#  \brief   Stores information about each routine
class Routine:
	'Stores the performers, the duration, and order of a routine'
	
	## 
	# \param[in] name         A name as a string
	# \param[in] performers   A list of performers as strings,
	# \param[in] duration     (OPTIONAL) the number of seconds in the routine as an int,
	# \param[in] order        (OPTIONAL) the routine number in the schedule. If no routine number is
	#                             specified, one will be determined and assigned to it.
	# \param[in] energy       (OPTIONAL) if the routine is high energy,
	def __init__(self, name = '', performers = [], duration = sys.maxsize, order = sys.maxsize, 
				 energy = True):

		self.name = name
		self.performers = performers
		self.energy = energy
		self.duration = duration
		self.order = order
		for perf in self.performers:
			perf.routines.append(self)
			perf.routines = list(set(perf.routines))

	##
	#  \brief Format a Routine by printing order, name, duration, and performers. Example:
	#  \code
	#  5. Dance 1
	#    Duration: 250 seconds
	#    Performers:
	#     * Performer 0
	#     * Performer 1
	#  \endcode
	#
	#  \remark Same output as the \ref toString function
	def __repr__(self):
		return self.toString()

	##
	#  \brief Returns whether the performer is in the routine
	#
	#  \param[in] perf      The performer
	def __contains__(self, perf):
		return perf in self.performers

	def __lt__(self, other):
		return self.score() < other.score()

	def __le__(self, other):
		return self.score() <= other.score()

	def __gt__(self, other):
		return self.score() > other.score()

	def __ge__(self, other):
		return self.score() >= other.score()

	# def __eq__(self, other):
	# 	if (self.name == other.name and self.energy == other.energy and 
	# 		self.duration == other.duration and self.order == other.order):
	# 		for i in range(len(self.performers)):
	# 			if self.performers[i] != other.performers[i]:
	# 				return False
	# 		return True

	##
	#  \return A string representation of the Routine
	#
	#  \brief Format a Routine by printing order, name, duration, and performers. Example:
	#  \code
	#  5. Dance 1
	#    Duration: 250 seconds
	#    Performers:
	#     * Performer 0
	#     * Performer 1
	#  \endcode
	def toString(self):
		output = str(self.order) + ": " + self.name + "\n"
		output += "  Duration:   " + str(self.duration) + " seconds\n"
		output += "  Performers:\n"

		for performer in self.performers:
			output += "   * " + performer.name + ": " + str(performer.score()) + "\n"
		return output

	## 
	#  \param[in] A routine
	#  \return    A list of performers in both routines
	#  \brief     Determines if the input routine has a at least one performer in common with self
	def samePerformers(self, routine):
		output = []
		for performer in self.performers:
			if performer in routine.performers:
				output.append(performer)
		return output

	## 
	#  \return  The score of the routine as an int
	#  \note    Currently just the summation of performer scores. Will add in duration at some point
	def score(self):
		output = 0
		for i in range(len(self.performers)):
			output += self.performers[i].score()
		return output


## \class Scheduler
#
#  \brief Calculates the order of routines optimizing rest for each performer and alternation of
#         energy of routines.
#
#  \warning May not find the most optimized schedule
class Scheduler:
	'Stores all of the Routines and determines the optimal order of routines.'

	## 
	#  \param[in] routines      A list of Routine objects
	#  \param[in] interLength   (OPTIONAL) The length of the intermission in seconds as an integer
	#  \param[in] interOrder    (OPTIONAL) The position of the intermission as an int
	#
	#  \remark Automatically places the intermission at the midway point in the schedule
	def __init__(self, routines = [], interLength = 900, interOrder = None):
		self.routines = routines
		self.schedule = [Routine('',[])] * (len(self.routines) + 1)
		self.performers = set()
		self.unused = []
		if interOrder != None:
			self.schedule[interOrder] = Routine('Intermission', [], intermLength, interOrder)

		# Places routines with specified positions. Store the index of of others in routines
		for i in range(len(self.routines)):
			if self.routines[i].order < len(self.schedule):

				# If something is already in that position, break
				if self.schedule[self.routines[i].order].order == self.routines[i].order:
					try:
						raise Exception(self.schedule[self.routines[i].order], self.routines[i])
					except Exception as inst:
						x,y = inst.args
						print("Tried to assign multiple routines to the same position")
						print("Original:\n" + x + "\n")
						print("Attempted:\n" + y + "\n")
				self.schedule[self.routines[i].order] = self.routines[i]
			else:
				self.unused.append(i)

			self.performers.update(self.routines[i].performers)

		self.performers = list(self.performers)

		# Find a place for the intermission as close to the center as possible
		# Iteratively expand outward from the middle of the list
		if interOrder == None:
			interOrder = len(self.schedule) // 2
			counter = 0
			while ( interOrder < len(self.schedule) and interOrder >= 0 and 
				self.schedule[interOrder].order != sys.maxsize ):
				if counter % 2 == 0:
					interOrder -= counter
				else:
					interOrder += counter
				counter += 1
			self.schedule[interOrder] = Routine('Intermission', [], interLength, interOrder)

	## 
	#  
	def __repr__(self):
		
		output = ""
		for routine in self.schedule:
			output += routine.toString()
		return output
		
	## 
	#  \param[in] routInd0  The index of the first routine in the scheduler
	#  \param[in] routInd1  The index of the second routine in the scheduler
	#  \param[in] schedule  (OPTIONAL) A proposed schedule. Defaults to the stored on if one 
	#                          isn't given
	#  \param[in] rout0     (OPTIONAL) The first routine. Necessary if routine hasn't been set in 
	#                          the schedule
	#  \param[in] rout1     (OPTIONAL) The second routine. Necessary if routine hasn't been set in 
	#                          the schedule
	def score2routines(self, routInd0, routInd1, schedule = None, 
		rout0 = None, rout1 = None):
		if schedule == None:
			schedule = self.schedule
		if rout0 == None:
			rout0 = schedule[routInd0]
		if rout1 == None:
			rout1 = schedule[routInd1]
		output = rout0.score() + rout1.score()

		same = rout0.samePerformers(rout1)

		# If there is no performer in both routines, the routines can go essentially anywhere 
		# relative to each other. Preference only based on energy.
		if same == []:
			output = sys.maxsize
			if 	abs(routInd0 - routInd1) == 1 and not rout0.energy and not rout1.energy:
				output -= 1
			return output

		priorityScale = 0
		for i in range(len(same)):
			priorityScale += same[i].score()
		for i in range(routInd0+1, routInd1):

			# If the routines between the input routines are not set, guess their durations to be the
			# same as the first input routine's
			if schedule[i].duration == sys.maxsize:
				output += priorityScale * (rout0.duration + rout1.duration) // 2
			else:
				output += priorityScale * schedule[i].duration

		if abs(routInd0 - routInd1) == 1 and not rout0.energy and not rout1.energy:
			output += rout0.duration + rout1.duration

		return output

	##
	#  \brief Scores a schedule given a routine and a position. Should be used to see how well a 
	#         routine scores at a particular position of the schedule.
	#
	#  \param[in] rout      A routine
	#  \param[in] pos       The position of the routine in the schedule as an int
	#  \param[in] schedule  The trial schedule as a list of routines
	def scoreRoutInSched(self, rout, pos, schedule = None):
		if schedule == None:
			schedule = self.schedule

		# If a different routine is already in that position, error
		if schedule[pos].name != '' and schedule[pos] != rout:
			try:
				raise Exception(self.schedule[pos], rout)
			except Exception as inst:
				x,y = inst.args
				print("Tried to score multiple routines in the same position")
				print("Original:\n" + x.toString() + "\n")
				print("Attempted:\n" + y.toString() + "\n")

		# Give score based on all scheduled routines
		score = 0
		for i in range(len(schedule)):
			if i == pos or schedule[i] == Routine('',[]):
				continue
			else:
				score += self.score2routines(i, pos, schedule, schedule[i], rout)
		return score


	## 
	#  \param[in] schedule      (OPTIONAL) A proposed schedule as a list of routines
	#  \return                  The score for the current permutation as an integer
	#  \brief                   Takes into count the amount of rest each performer gets scaled by 
	#                           their priority score as well as reducing the amount of consecutive 
	#                           low energy performances
	def scoreSchedule(self, schedule = None):
		if schedule == None:
			schedule = self.schedule

		output = 0

		# For each performer, find the amount of rest between each routine
		for perf in self.performers:
			rest = 0
			for i in range(len(perf.routines) - 1):

				# If routines are consecutive, rest score based on the length of the performances
				if perf.routines[i].order - perf.routines[i+1].order <=1:
					rest -= perf.routines[i].duration + perf.routines[i+1].duration

				for j in range(perf.routines[i].order + 1, perf.routines[i+1].order):
					rest += schedule[j].duration

			# Scale the amount of rest based on score of the performer. May need adjustment by a
			# constant factor
			output += rest * perf.score()

		# If consecutive routines are low energy, add the durations of the routines. Will double 
		# count all but first and last consecutive low energy routines
		for i in range(len(schedule) - 1):
			if not schedule[i].energy and not schedule[i+1].energy:
				output += schedule[i].duration + schedule[i+1].duration

		return output

	##
	#  Finds a possible schedule for the performance. Modifies the stored schedule list in self as
	#  well as the routines themselves (only the order)
	#
	def sortRoutines(self):
		self.schedule = self.sortHelper(self.schedule, self.unused)

		# Set the routine's orders
		for i in range(len(self.schedule)):
			if self.schedule[i].order != i:

				# If the routine's placed order is different than the user specified order, error
				if self.schedule[i].order < len(self.schedule):
					try:
						raise Exception(self.schedule[i])
					except Exception as inst:
						print("Moved a set routine:\n")
						print(inst.args)
				self.schedule[i].order = i


	##
	#  \brief Used by sortRoutines to recursively determine the schedule
	#  
	#  \param[in] schedule  A list of ordered routines
	#  \param[in] unused    A list of indices of routines that are not yet in schedule. The indices
	#                       correspond to the list self.routines
	#  \param[in] n         The number of positions the routines should be tried in
	def sortHelper(self, schedule, unused, n = 3):
		# print("------------------------------------------------------")
		if unused == []:
			return schedule

		# Find the highest priority unused routine
		ind = unused.index(max(unused, key=lambda x: self.routines[x]))
		rout = self.routines[unused[ind]]

		# Find the n best positions for the routine
		pos = [0] * min(n, len(unused))
		scores = [0] * len(pos)

		for i in range(len(schedule)):
			# print(i)
			# print(schedule[i])
			# print(schedule[i].name == '')
			if schedule[i].name == '':
				score = self.scoreRoutInSched(rout, i, schedule)
				# print("score: ", score)

				# check previous n best
				for j in range(len(pos)):
					if score > scores[j]:
						scores = scores[:j] + [score] + scores[j+1:-1]
						pos = pos[:j] + [i] + pos[j+1:-1]
						break
		# print(unused[:ind] + unused[ind + 1:])
		# print([self.routines[i] for i in unused[:ind] + unused[ind + 1:]])
		# print(schedule)

		scheds = []
		# print(pos)
		# print("===================================================")
		for i in range(len(pos)):
			scheds.append(self.sortHelper(schedule[:pos[i]] + [rout] + schedule[pos[i] + 1:],
				unused[:ind] + unused[ind + 1:]))
		return max(scheds, key=lambda x: self.scoreSchedule(x))
