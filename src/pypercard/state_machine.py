"""
PyperCard is a simple HyperCard inspired framework for PyScript for building
graphical apps in Python.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2023 Anaconda Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class Machine:
    """A simple Finite State Machine (FSM) implementation."""

    def __init__(
        self,
        model,
        states=None,
        transitions=None,
        state_name="",
        history=None,
        context=None,
    ):
        """Constructor."""

        # For convenience, we allow each state to be passed as either:-
        #
        # a) A State instance.
        # b) A tuple of constructor arguments for the State class.
        self.states = [
            state if isinstance(state, State) else State(*state)
            for state in states or []
        ]

        # For convenience, we allow each transition to be passed as either:-
        #
        # a) A Transition instance.
        # b) A tuple of constructor arguments for the Transition class.
        self.transitions = [
            transition
            if isinstance(transition, Transition)
            else Transition(*transition)
            for transition in transitions or []
        ]

        self.model = model
        self.state_name = state_name
        self.history = history or []
        self.context = context or {}

        # Make it quicker to lookup states by name :)
        self._states_by_name = {state.name: state for state in self.states}

    @property
    def current_state(self):
        """Return the current state."""

        return self._states_by_name[self.state_name]

    @property
    def is_done(self):
        """Return True iff there are no transitions out of the current state.

        The machine inherently has no notion of success or failure - it only
        knows whether there is any possible way out of the current state. The
        state machine writer can add meaning to the 'done' states with naming
        conventions and/or state subclasses etc.

        """

        return not any(
            [
                (
                    transition.source == self.state_name
                    or transition.source == "*"
                )
                for transition in self.transitions
            ]
        )

    def add_state(self, state, transitions=None):
        """Add a state and (optionally) its transitions to the machine."""

        self.states.append(state)
        self.transitions.extend(transitions or [])

        self._states_by_name = {state.name: state for state in self.states}

    def goto(self, state_name, run_hooks=True):
        """Goto a specific state.

        This calls any on exit hooks on the current state and any on enter
        hooks on the target state.

        """

        state = self._states_by_name.get(state_name)
        if state is None:
            raise ValueError(f"No such state: {state}")

        # Exit the current state...
        if run_hooks:
            self._exit_state(state)

        # ... and enter the new one.
        self.state_name = state_name
        if run_hooks:
            self._enter_state(self.current_state)

        return state_name

    def next(self, input_):
        """Attempt to transition from the current state with the given input.

        Return either:-

        1) the name of the state we transitioned to.
        2) an empty string if a transition accepted the input but didn't move
           state.
        3) null if no transition accepted the input.

        """
        if self.is_done:
            self.pprint()
            raise ValueError(
                f"Machine is already done but got input: {input_}"
            )

        for transition in self.transitions:
            if (
                transition.source == "*"
                or transition.source == self.state_name
            ):
                # We use the first transition that accepts the input.
                if transition.accepts(self, input_):
                    return self._do_transition(transition, input_)

        # No transition handled the input.
        # print('No transition handled input:', input_)
        return ""

    def history_pop_previous(self):
        """Return the name of the previous state in the history.

        This pops the current and previous states from the history ready for
        the transition to the previous state (where the previous state will get
        added to the history).

        TODO: This only works if this method is called from a transition...

        """

        if len(self.history) < 2:
            raise ValueError(f"No previous state: {self.history}")

        # Remove the current state from the history...
        self.history.pop()

        # Remove the previous state we are going back to from the history too
        # as it gets added again when we go there.
        return self.history.pop()

    def start(self, state_name=None):
        """Start the machine."""

        # If no start state was specified then use the first one in the list
        # of states.
        self.state_name = state_name or self.state_name or self.states[0].name

        self._enter_state(self.current_state)

    def pprint(self, indent=""):
        """Pretty-print the object."""

        print(
            f"{indent}{type(self).__name__}({self.model}, "
            f"{self.state_name}, {self.context})"
        )

        indent += "  "
        for state in self.states:
            state.pprint(indent)

        for transition in self.transitions:
            transition.pprint(indent)

    def _do_transition(self, transition, input_):
        """Do the specified transition!"""

        # Transitions can add to the context... we do it here in case any of
        # the transition hooks want to use the value.
        if transition.context_object_name:
            self.context[
                transition.context_object_name
            ] = transition.get_context_object(self, input_)

        # Pre-transition hooks.
        transition.call_before_hooks(self, input_)

        # Where are we heading next? :)
        next_state_name = transition.get_target(self, input_)

        # A transition can accept the input but NOT move to another state by
        # returning anything "falsey" (e.g. an empty string or None). This
        # allows transition hooks to be run without changing state.
        if next_state_name:
            # Exit the current state...
            self._exit_state(self.current_state)

            # ... and enter the new one.
            self.state_name = next_state_name
            self._enter_state(self.current_state)

        # Post-transition hooks.
        transition.call_after_hooks(self, input_)

        return next_state_name

    def _enter_state(self, state):
        """Enter the specified state."""

        state.call_on_enter_hooks(self)
        self.history.append(state.name)

    def _exit_state(self, state):
        """Exit the specified state."""

        state.call_on_exit_hooks(self)


class State:
    """A state in a state machine :)"""

    def __init__(self, name, on_enter=None, on_exit=None):
        """Constructor."""

        self.name = name
        self.on_enter = on_enter or []
        self.on_exit = on_exit or []

    def pprint(self, indent=""):
        """Pretty-print the object."""

        print(
            f'{indent}{type(self).__name__}("{self.name}", '
            f"on_enter={self.on_enter}, on_exit={self.on_exit})"
        )

    # TODO: async?
    def call_on_enter_hooks(self, machine):
        """Call all on_enter hooks."""

        for hook in self.on_enter:
            hook(machine)

    # TODO: async?
    def call_on_exit_hooks(self, machine):
        """Call all on_exit hooks."""

        for hook in self.on_exit:
            hook(machine)


class Transition:
    """A possible transition from one state to another."""

    def __init__(
        self,
        source,
        acceptor,
        target=None,
        context_object_name="",
        before=None,
        after=None,
    ):
        """Constructor.

        If 'source' is the string '*' then it is a possible transition from
        *any* state.

        """

        self.source = source
        self.acceptor = (
            acceptor if isinstance(acceptor, Acceptor) else Acceptor(acceptor)
        )
        self.target = target
        self.context_object_name = context_object_name
        self.before = before or []
        self.after = after or []

    def pprint(self, indent=""):
        """Pretty-print the object."""

        print(
            f'{indent}{type(self).__name__}("{self.source}", {self.acceptor}, '
            f'"{self.target}", "{self.context_object_name}", '
            f"before={self.before}, after={self.after})"
        )

    def accepts(self, machine, input_):
        """Return True iff the specified input is accepted.

        By default, this simply calls the transition's acceptor.

        """

        return self.acceptor.accepts(machine, input_)

    def get_context_object(self, machine, input_):
        """Return the object to add to the machine's context iff this
        transition succeeds.

        By default, we delegate this to the acceptor since state machine
        builders usually build acceptors, not transitions.

        """

        return self.acceptor.get_context_object(machine, input_)

    def get_target(self, machine, input_):
        """Get the target state name."""

        if callable(self.target):
            return self.target(machine, input_)

        return self.target

    # TODO: async?
    def call_before_hooks(self, machine, input_):
        """Call any before hooks."""

        for hook in self.before:
            hook(machine, input_)

    # TODO: async?
    def call_after_hooks(self, machine, input_):
        """Call any before hooks."""

        for hook in self.after:
            hook(machine, input_)


class Acceptor:
    """Acceptors determine whether the received input is allowed."""

    def __init__(self, fn=None):
        """Constructor."""

        self.fn = fn

    def __str__(self):
        """Pretty-print the object."""

        return (
            f"{type(self).__name__}"
            f'({self.fn.__name__ if self.fn is not None else ""})'
        )

    def accepts(self, machine, input_):
        """Return True iff the specified input is accepted.

        If no function 'fn' is specified this defaults to returning true (i.e.
        it accepts *everything* :) ).

        """

        # If the 'fn' attribute is set call that. This allows to us to
        # implement acceptors without the need for subclassing.
        if self.fn is not None:
            return self.fn(machine, input_)

        return True

    def get_context_object(self, machine, input_):
        """Return the object to add to the machine's context iff this acceptor
        accepts!"""

        return input_
