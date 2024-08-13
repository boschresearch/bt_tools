## Transform a behavior tree into a finite state machine

This tutorial will teach you how to use the algorithm in this package to transform a behavior tree into a functionally equivalent finite state machine.

### Background

This implements the algorithm described in [_Behavior Trees in Robotics and AI: An Introduction_ by Michele Colledanchise, Petter Ögren](https://arxiv.org/pdf/1709.00084).
Of particular interest is the section __2.2.2 Creating a FSM that works like a BTs__ (page 29).

For our implementation, please refer to [the Bt2FSM class](https://bt-tools.readthedocs.io/en/latest/apidocs/btlib/btlib.bt_to_fsm.bt_to_fsm.html#btlib.bt_to_fsm.bt_to_fsm.Bt2FSM).

### Prerequisites

You need to have this package installed in your workspace.
If you don't have it, build it:

```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone https://github.com/boschresearch/bt_tools.git
cd ~/catkin_ws
catkin build --symlink-install --packages-select btlib
source ~/catkin_ws/devel/setup.bash
```

### Input file

You can pass any behavior tree in the [behaviortree.cpp](https://behaviortree.dev) format to the algorithm.
For example [simple_bt.xml](https://github.com/boschresearch/bt_tools/blob/main/btlib/test/_test_data/bt2fsm/simple_bt.xml):

```xml
<root BTCPP_format="4">
    <BehaviorTree>
        <Sequence>
            <ServiceBtCondition name="TEST_CONDITION" />
            <Fallback>
                <ActionBtAction name="TEST_ACTION_A" />
                <ActionBtAction name="TEST_ACTION_B" />
            </Fallback>
        </Sequence>
    </BehaviorTree>
</root>
```

### Call the algorithm

Then pass it to the script:

```bash
bt_to_fsm.py ~/catkin_ws/src/bt_tools/btlib/test/_test_data/bt2fsm/simple_bt.xml
```

### Output

This will generate a file called `fsm.png` in your current directory.
It will look something like this:

![FSM](imgs/fsm.png)