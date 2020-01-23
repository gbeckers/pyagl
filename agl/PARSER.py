#######################
# Explanation of terms:
#######################
#
# percept_shaper
# --------------
# From Perruchet and Vinter (1998): "percept shaper (PS). PS is composed of
# the internal representations of the displayed material and may be
# thought of as a memory store or a mental lexicon. A weight, which reflects
# the person’s familiarity with the item, is assigned to each element in PS.
# At the start of the familiarization session, PS contains only the
# primitives needed for processing the material (i.e., a few syllables). At
# the end, it should contain, in addition, all the words and legal clauses
# (i.e., units combining a few words) of the language. During the shaping
# process, PS may contain a mixture of words and legal clauses, part-words
# (e.g., two syllables out of a three-syllable word), and nonwords (e.g.,
# the last syllable of one word with the first syllable of another word).
#
# primitive
# ---------
# The base elements from which word are built. This is also called a
# syllable in the paper.
#
# syllable
# --------
# Same as primitive.
#
# unit
# ----
# a sequence of syllables/primitives (normally of length 1-3) that is
# stored in memory (i.e. in the percept shaper). These can be "words and legal
# clauses, part-words (e.g., two syllables out of a three-syllable word),
# and nonwords (e.g., the last syllable of one word with the first syllable of
# another word)
#
# percept
# -------
# a sequence of syllables/primitives that is perceived and processed for
# shaping in one time step.


__all__ = ['PARSER']

import random
import sys
import logging

from collections import defaultdict
from .strfuncs import lengthnsubstrings


class PARSER:
    """PARSER: The PARSER model for word segmentation

    A python implementation of the word segmentation model by Pierre Perruchet
    and Annie Vinter (1998).

    Parameters
    ----------
    primitives: list
        List of primitives from which words are build.
    perceptshaper: dict or None
        A dictionary with percept strings and their weights. E.g. {'abc': 0.3,
        'cde': 0.5}. Defaults is None, meaning that percepts should be built
        from scratch.
    shapingthreshold: float
        The threshold a percept has to cross to be perceived from input.
        Defaults to 1.0
    newunitweight: float
        The weight that a new unit gets when it becomes part of the percept
        shaper. Defaults to 1.0
    forgetweigtht: float
        The weight that is added (normally a negative number) so that the
        percept shaper increasingly forgets units. Defaults to -0.05
    consolidationweight: float
        The weight that is added to an existing unit in the percept shaper
        when it is used to shape perception. Defaults to 0.5
    interferenceweight: float
        The weight that is added (normally a negative number) to units in
        the percept shaper that share primitives with a perceived unit.
        Defaults to -0.005
    minperceptsize: int
        The minimum number of percepts that are perceived in one
        step (should be at least 1). Defaults to 1
    maxperceptsize: int
        The maximum number of percepts that are perceived in one
        step (should be at least 1). Defaults to 3
    randomseed: int or None
        The seed for the random generator. Use for repeatability. If None,
        the current system time is used. Default is None.
    readingframe: positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "a1a2" has two tokens, namely "a1" and "a2".
    logginglevel: int
        Sets the threshold for logger to givenlevel. Logging messages which
        are less severe than level will be ignored; logging messages which have
        severity level or higher will be emitted by whichever handler or
        handlers service this logger, unless a handler’s level has been set to
        a higher severity level than level.Defaults to logging.CRITICAL (50)

    References
    ----------
    Perruchet, P. and Vinter, A. (1998). PARSER: A PARSER for Word
    Segmentation. *Journal of Memory and Language*, 39, 246–263 (1998)

    """
    def __init__(self, primitives, perceptshaper=None, shapingthreshold=1.0,
                 newunitweight=1.0, forgetweight=-0.05, consolidationweight=0.5,
                 interferenceweight=-0.005, minperceptsize=1, maxperceptsize=3,
                 randomseed=None, readingframe=1, logginglevel=logging.CRITICAL):
        if len(primitives) == 0:
            raise ValueError("`primitives` parameter cannot be empty")
        else:
            for p in primitives:
                if len(p) != readingframe:
                    raise ValueError(f"primitive {p} does not conform to  "
                                     f"a readingframe of {readingframe}")
        self._primitives = set(primitives)
        self._readingframe = readingframe
        self._forgottenprimitives = set()
        self._perceptshaper = {}
        if perceptshaper is not None:
            self._perceptshaper.update(perceptshaper)
        self._shapingthreshold = shapingthreshold
        self._newunitweight = newunitweight
        self._forgetweight = forgetweight
        self._consolidationweight = consolidationweight
        self._interferenceweight = interferenceweight
        self._minperceptsize = minperceptsize
        self._maxperceptsize = maxperceptsize
        #FIXME this can't be correct
        if randomseed is not None:
            randomseed = random.randrange(sys.maxsize)
        self._randomseed = randomseed
        self._random = random.Random(self._randomseed)
        self._stepno = 0 # counter to keep track of how many steps were done
        self._weightdeltas = {} # cleared each step; used to keep track of weight adjustments
        self._novelunits = set({})
        self.logger = logging.getLogger()
        self.logger.setLevel(logginglevel)

    @property
    def readingframe(self):
        return self._readingframe

    @property
    def perceptshaper(self):
        """Dictionary with percepts (chunks) as keys and weights as values"""
        return self._perceptshaper

    @property
    def shapingthreshold(self):
        """The threshold a percept has to cross to be perceived from input."""
        return self._shapingthreshold

    @property
    def newunitweight(self):
        """The weight that a new unit gets when it becomes part of the percept
        shaper."""
        return self._newunitweight

    @property
    def forgetweight(self):
        """The weight that is added (normally a negative number) so that the
        percept shaper increasingly forgets units."""
        return self._forgetweight

    @property
    def consolidationweight(self):
        """The weight that is added to an existing unit in the percept shaper
        when it is used to shape perception."""
        return self._consolidationweight

    @property
    def interferenceweight(self):
        """The weight that is added (normally a negative number) to units in
        the percept shaper that share primitives with a perceived unit."""
        return self._interferenceweight

    @property
    def minperceptsize(self):
        """The minimum number of percepts that are perceived in one
        step (should be at least 1)"""
        return self._minperceptsize

    @property
    def maxperceptsize(self):
        """The maximum number of percepts that are perceived in one
        step (should be at least 1)"""
        return self._maxperceptsize

    @property
    def primitives(self):
        """list of primitives (='syllables')"""
        return self._primitives

    @property
    def randomseed(self):
        return self._randomseed


    def run(self, inputstring, perceptsizes=None):
        """Run PARSER model instance on input string, based on current
        parameter properties and potentially already learned chunks in
        perceptshaper.

        Parameters
        ----------
        inputstring: str
            The string of tokens to run the model on.
        perceptsizes: iterable of ints or None
            A sequence of percept sizes that should be used in each step.
            This is predominantly useful when debugging, inspecting or
            verifying every step in a deterministic way, e.g. to compare it
            to other implementations such as the original PARSER software by
            Perruchet
            .
        Returns
        -------
        str
            Remainder of string that is not processed.

        """
        remainder = inputstring
        if perceptsizes is not None:
            perceptsizes = (s for s in perceptsizes)
        while remainder:
            if perceptsizes is not None:
                perceptsize = next(perceptsizes)
            else:
                perceptsize = None
            remainder = self._run_step(remainder, nunits=perceptsize)
        return remainder

    def _run_step(self, inputsequence, nunits=None):
        """Runs one iteration on the inputsequence, perceiving the first
        random n items (between min_percept_size and max_percept_size),
        and undergoing interference and forgetting. I.e. a step is the
        processing of one percept, corresponding to one cycle in Fig
        1. of Perruchet & Vinter.

        Private method, normally not to be used by external user. Use the
        `run` method instead.

        Parameters
        ----------
        inputsequence: str

        Returns
        -------
        str:
            remainderstring, what remains after the first part of the
            inputstring is processed

        """
        self._stepno += 1
        ps = self.perceptshaper
        # clear novelunits and weightdeltas. These keep track of which units
        # are novel in one cycle (step) and of unit weight changes that
        # accumulate over the course of a cycle. These changes do not take
        # effect during the cycle, but only at the end of it.
        self._novelunits = set()
        self._weightdeltas = wd = defaultdict(float)
        self.logger.info(f'START STEP {self._stepno}\n'
                         f'\thead of input sequence: {inputsequence[:30]}...\n'
                         f'\tpercept shaper at start step: {ps}')
        # step a: select randomly the size of the next percept
        if nunits is None:
            nunits = self._random.randint(self.minperceptsize,
                                          self.maxperceptsize)
        perceivedunits, remainder = self._perceive(nunits, inputsequence)
        percept = ''.join(perceivedunits)
        self.logger.info(f'\tpercept: {percept}')
        # step b:
        if percept in ps:
            if ps[percept] >= self.shapingthreshold:
                wd[percept] += self.consolidationweight
            else:
                wd[percept] += self.newunitweight
        elif percept in self.primitives:
            if percept not in self._forgottenprimitives:
                self._novelunits.add(percept)
        else: # new non-primitive percept
            self._novelunits.add(percept)
        if len(perceivedunits) > 1: # add weights to components
            for unit in perceivedunits:
                if unit in ps:
                    if ps[unit] >= self.shapingthreshold:
                        wd[unit] += self.consolidationweight
                    else:
                        wd[unit] += self.newunitweight
                elif (unit in self.primitives) and \
                     (unit not in self._forgottenprimitives):
                    self._novelunits.add(unit)
        self._interfere(perceivedunits=perceivedunits)
        self._forget()
        # effectuate all changes at the end of the cycle: changing
        # weights, removing units, adding units etc.
        for unit in self._novelunits:
            ps[unit] = self.newunitweight
        for unit, delta in wd.items():
            ps[unit] += delta
            if ps[unit] <= 0:
                self.logger.info(f'\tremoving {unit} with weight <= 0 '
                                 f'({ps[unit]})')
                ps.pop(unit)
                if unit in self.primitives:
                    self._forgottenprimitives.add(unit)
        self.logger.info(f'\tpercept shaper at end step: {ps}\n'
                         f'END STEP')
        return remainder

    def _perceive(self, nunits, inputsequence):
        """Perceive units from input sequence of primitives.

        Private method, normally not to be used by external user. Use the
        `run` method instead.

        Parameters
        ----------
        nunits: int
            The number of units to perceive from the head of the
            inputsequence. A unit is a (usually short, 1-3) sequence of
            primitives.
        inputsequence: str
            The sequence of primitives that are perceived. The remainder of
            the sequence is returned.

        Returns
        -------
        tuple (perceived units, remainder of input sequence)

        """
        minweight = self.shapingthreshold
        memoryunits = [unit for unit, weight in self.perceptshaper.items()
                       if weight > minweight]
        self.logger.info('\tSTART PERCEIVE\n'
                         f'\t\tmemory units: {memoryunits}')
        if memoryunits:
            maxperceptlength = max(map(len, memoryunits))
        else:
            maxperceptlength = self.readingframe
        perceivedunits = []
        remainder = inputsequence
        for i in range(nunits):
            if maxperceptlength > len(remainder):
                maxperceptlength = len(remainder)
            candidate = remainder[:maxperceptlength]
            while candidate not in memoryunits and len(candidate) > self.readingframe:
                if candidate in self.primitives:
                    perceivedunits.append(candidate)
                    break
                else:
                    candidate = candidate[:-self.readingframe]
            remainder = remainder[len(candidate):]
            if candidate != "":
                perceivedunits.append(candidate)
        self.logger.info(f'\t\tperceived units: {perceivedunits}\n'
                         f'\t\tremainder at end perceive: {remainder[:30]}...\n'
                         f'\tEND PERCEIVE')
        return perceivedunits, remainder

    def _interfere(self, perceivedunits):
        iw = self.interferenceweight
        ps = self.perceptshaper
        wd = self._weightdeltas
        rf = self.readingframe
        shth = self.shapingthreshold
        self.logger.info(f'\tSTART INTERFERE')
        valperceivedunits = [u for u in perceivedunits if u in ps and ps[u] > shth]
        targets = set(self.perceptshaper.keys()) - self._novelunits
        self.logger.info(f'\t\ttargets: {targets}')
        for perceivedunit in valperceivedunits:
            for targetunit in targets:
                if perceivedunit != targetunit:
                    iprimitives = lengthnsubstrings(perceivedunit, 1,
                                                    readingframe=rf)
                    nmatches = sum(targetunit.count(ip) for ip in iprimitives)
                    if nmatches > 0:
                        self.logger.info(f'\t\t{nmatches} interferences in '
                                         f'{targetunit}')
                        wd[targetunit] += nmatches * iw
        self.logger.info(f'\tEND INTERFERE')

    def _forget(self):
        """Decrease the weights of non novel units in percept shaper with a
        fixed amount, as defined by the `forgetting_weight` parameter of the
        model. This is a negative value that is added to the current weight.

        According to Fig 1 of Perruchet & Vinter 1998 the weight of all units
        in the percept shaper decrease by a fixed amount in every cycle
        (default 0.05). However in the original implementation provided by
        the authors, units are not decreased when they are new and have just
        been added to the percept shaper. I.e. they get their initial weight
        (default 1) and there is no forgetting in that cycle. This is true
        for new chunks and for primitives when they are perceived the first
        time.

        Another behavior of the original implementation that is not
        entirely clear from the paper is that primitives with a weight below 0
        are removed from the percept shaper and *do not return*. Units
        consisting of multiple primitives (chunks) are also removed, but *can
        return* if they are perceived again.

        """
        self.logger.info(f'\tSTART FORGET')
        ps = self.perceptshaper
        wd = self._weightdeltas
        for unit, weight in list(ps.items()):
            if unit not in self._novelunits:
                wd[unit] += self.forgetweight
        self.logger.info(f'\tEND FORGET')
