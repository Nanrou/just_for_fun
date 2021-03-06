package headFirst.Proxy.Gumball;

import java.rmi.*;
import java.rmi.server.*;

import headFirst.Proxy.GumballMachineRemote;

public class GumballMachine extends UnicastRemoteObject implements GumballMachineRemote {
//    final static int SOLD_OUT = 0;  // 糖果售罄
//    final static int NO_QUARTER = 1;  // 没有塞钱
//    final static int HAS_QUARTER = 2;  // 已经塞钱了
//    final static int SOLD = 3;  // 售出糖果
//
//    int state = SOLD_OUT;
//    int count = 0;
//
//    public GumballMachine(int count) {
//        this.count = count;
//        if (count > 0) {
//            state = NO_QUARTER;
//        }
//    }
//
//    public void insertQuarter() {  // 塞钱这个动作
//        if (state == HAS_QUARTER) {
//            System.out.println("You can't insert another quarter");
//        } else if (state == NO_QUARTER) {
//            System.out.println("You inserted a quarter");
//            state = HAS_QUARTER;
//        } else if (state == SOLD_OUT) {
//            System.out.println("You can't insert a quarter");
//        } else if (state == SOLD) {
//            System.out.println("Please wait, we're already giving you a gumball");
//        }
//    }
//
//    public void ejectQuarter() {  // 想要退钱
//        if (state == HAS_QUARTER) {
//            System.out.println("Quarter returned");
//            state = NO_QUARTER;
//        } else if (state == NO_QUARTER) {
//            System.out.println("You haven't inserted a quarter");
//        } else if (state == SOLD_OUT) {
//            System.out.println("You can't eject, you haven't inserted a quarter yet");
//        } else if (state == SOLD) {
//            System.out.println("Sorry, you already turned the crank");
//        }
//    }
//
//    public void turnCrank() {  // 扭动开关
//        if (state == HAS_QUARTER) {
//            System.out.println("You turned...");
//            state = SOLD;
//            dispense();
//        } else if (state == NO_QUARTER) {
//            System.out.println("You turned but there's no quarter");
//        } else if (state == SOLD_OUT) {
//            System.out.println("You turned, but there are no gumballs");
//        } else if (state == SOLD) {
//            System.out.println("Turning twice doesn't get you another gumball");
//        }
//    }
//
//    public void dispense() {  // 分发糖果
//        if (state == SOLD) {
//            System.out.println("A gumball comes rolling out the slot");
//            count -= 1;
//            if (count == 0) {
//                System.out.println("Oops, out of gumballs!");
//                state = SOLD_OUT;
//            } else {
//                state = NO_QUARTER;
//            }
//        } else if (state == HAS_QUARTER) {
//            System.out.println("No gumball dispensed");
//        } else if (state == NO_QUARTER) {
//            System.out.println("You need to pay first");
//        } else if (state == SOLD_OUT) {
//            System.out.println("No gumball dispensed");
//        }
//    }

    State soldOutState;
    State noQuarterState;
    State hasQuarterState;
    State soldState;
    State winnerState;

    State state = soldOutState;
    int count = 0;
    String location;

    public GumballMachine(int count, String location) throws RemoteException {
        soldOutState = new SoldOutState(this);
        noQuarterState = new NoQuarterState(this);
        hasQuarterState = new HasQuarterState(this);
        soldState = new SoldState(this);
        winnerState = new WinnerState(this);

        this.count = count;
        if (count > 0) {
            state = noQuarterState;
        }
        this.location = location;
    }

    public void setState(State state) {
        this.state = state;
    }

    public void insertQuarter() {  // 塞钱这个动作
        state.insertQuarter();
    }

    public void ejectQuarter() {  // 想要退钱
        state.ejectQuarter();
    }

    public void turnCrank() {  // 扭动开关
        state.turnCrank();
        state.dispense();
    }

    void releaseBall() {
        System.out.println("A gumball comes rolling out the slot...");
        if (count != 0) {
            count -= 1;
        }
    }

    public int getCount() {
        return count;
    }

    public State getState() { return state; }

    public String getLocation() { return location; }

    public State getHasQuarterState() {
        return hasQuarterState;
    }

    public State getNoQuarterState() {
        return noQuarterState;
    }

    public State getSoldOutState() {
        return soldOutState;
    }

    public State getSoldState() {
        return soldState;
    }

    public State getWinnerState() {
        return winnerState;
    }

    public void refill(int count) {
        this.count += count;
        state = noQuarterState;
    }

    @Override
    public String toString() {
        return "A GumballMachine with " + count + " gumball, which state is " + state + "\n";
    }
}
