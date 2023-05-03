import pytest
from js import document
from unittest import mock

from pypercard.state_machine import Machine, State, Transition


# An acceptor that ALWAYS accepts!
def always_accept(machine, transition, input_):
    assert type(machine) is Machine
    assert type(transition) is Transition
    return True


# AN Acceptor that NEVER accepts!
def never_accept(machine, transition, input_):
    assert type(machine) is Machine
    assert type(transition) is Transition
    return False


def test_cant_start_machine_without_any_states():
    """
    Can't start a machine if it doesn't contain any states.
    """

    # Given.
    machine = Machine()

    # When.
    with pytest.raises(ValueError) as exc:
        machine.start()

    # Then.
    assert str(exc.value) == "Can't start a machine without any states!"


def test_cant_start_machine_with_invalid_initial_state():
    """
    Can't start a machine if it doesn't contain a state with the specified
    initial state name.
    """

    # Given.
    machine = Machine(
        states=[
            State("state-1")
        ],
        initial_state_name="state-2"
    )

    # When.
    with pytest.raises(ValueError) as exc:
        machine.start()

    # Then.
    assert str(exc.value) == "No such state: state-2"


def test_cant_start_machine_with_invalid_start_state():
    """
    Can't start a machine if it doesn't contain a state with the specified start
    state name.
    """

    # Given.
    machine = Machine(
        states=[
            State("state-1")
        ]
    )

    # When.
    with pytest.raises(ValueError) as exc:
        machine.start("state-2")

    # Then.
    assert str(exc.value) == "No such state: state-2"


def test_start_machine_defaults_to_first_state():
    """
    If no start state is specified, then the machine should start in the first
    state in the list.
    """

    # Given.
    machine = Machine(
        states=[
            State("state-1"),
            State("state-2")
        ]
    )

    # When.
    machine.start()

    # Then.
    assert machine.current_state.name == "state-1"


def test_start_machine_uses_specified_initial_state():
    """
    If an initial state name is specified, then the machine should start there.
    """

    # Given.
    machine = Machine(
        states=[
            State("state-1"),
            State("state-2")
        ],
        initial_state_name="state-2"
    )

    # When.
    machine.start()

    # Then.
    assert machine.current_state.name == "state-2"


def test_start_machine_in_a_specific_state():
    """
    If a start state is specified, then the machine should start there.
    """

    # Given.
    machine = Machine(
        states=[
            State("state-1"),
            State("state-2")
        ]
    )

    # When.
    machine.start("state-2")

    # Then.
    assert machine.current_state.name == "state-2"


def test_input_doesnt_cause_a_transition():
    """
    If an input doesn't cause a transition, make sure we stay in the current
    state.
    """

    # Given.
    machine = Machine(
        states=[
            State("state-1"),
            State("state-2")
        ],
        transitions=[
            # A transition that NEVER accepts anything!
            Transition("state-1", never_accept, "state-2")
        ]
    )
    machine.start()

    # When.
    machine.next("anything")

    # Then.
    assert machine.current_state.name == "state-1"


def test_input_causes_a_transition_with_a_string_target():
    """
    If an input causes a transition that has a simple string target, make sure we
    go to the appropriate state.
    """

    # Given.
    machine = Machine(
        states=[
            State("state-1"),
            State("state-2")
        ],
        transitions=[
            Transition("state-1", always_accept, "state-2")
        ]
    )
    machine.start()

    # When.
    machine.next("anything")

    # Then.
    assert machine.current_state.name == "state-2"


def test_input_causes_a_transition_with_a_callable_target():
    """
    If an input causes a transition that has a callable target, make sure we
    call it and go to the appropriate state.
    """

    target = mock.MagicMock(return_value="state-2")

    # Given.
    machine = Machine(
        states=[
            State("state-1"),
            State("state-2")
        ],
        transitions=[
            Transition("state-1", always_accept, target)
        ]
    )
    machine.start()

    # When.
    machine.next("anything")

    # Then.
    target.assert_called_once_with(
        machine, machine.transitions[0], "anything"
    )
    assert machine.current_state.name == "state-2"


def test_state_on_enter_and_on_exit_hooks_are_called():
    """
    Make sure any state on enter and on exit hooks are called.
    """

    # Given.
    mock_on_enter = mock.MagicMock()
    mock_on_exit = mock.MagicMock()

    machine = Machine(
        states=[
            State("state-1", on_enter=[mock_on_enter], on_exit=[mock_on_exit]),
            State("state-2", on_enter=[mock_on_enter], on_exit=[mock_on_exit]),
        ],
        transitions=[
            # A transition that accepts anything!
            Transition("state-1", always_accept, "state-2")
        ]
    )

    # When.
    machine.start("state-1")

    # Then.
    mock_on_enter.assert_called_once_with(machine, machine.states[0])
    assert mock_on_exit.call_count == 0

    # When.
    machine.next("anything")

    # Then.
    assert mock_on_enter.call_count == 2
    mock_on_exit.assert_called_once_with(machine, machine.states[0])


def test_transition_before_and_after_hooks_are_called():
    """
    Make sure any transition before and after hooks are called.
    """

    # Given.
    mock_before = mock.MagicMock()
    mock_after = mock.MagicMock()

    machine = Machine(
        states=[
            State("state-1"),
            State("state-2"),
        ],
        transitions=[
            Transition(
                "state-1", always_accept, "state-2",
                before=[mock_before], after=[mock_after]
            )
        ]
    )
    machine.start()

    # When.
    machine.next("anything")

    # Then.
    expected_args = (machine, machine.transitions[0], "anything")

    mock_before.assert_called_once_with(*expected_args)
    assert mock_after.call_count == 1

    mock_after.assert_called_once_with(*expected_args)
    assert mock_after.call_count == 1


def test_transition_can_add_to_the_context():
    """
    If the transition specifies a context name then by default we add the input
    to the context with that name.
    """

    # Given.
    machine = Machine(
        states=[
            State("state-1"),
            State("state-2"),
        ],
        transitions=[
            # A transition that accepts anything!
            Transition(
                "state-1", always_accept, "state-2", context_object_name="x"
            )
        ]
    )
    machine.start()

    # When.
    machine.next("anything")

    # Then.
    assert machine.context.get("x") == "anything"
