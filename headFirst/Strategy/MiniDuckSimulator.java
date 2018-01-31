package headFirst.Strategy;

public class MiniDuckSimulator {
    public static void main(String[] args) {
        Duck mallard = new MallardDuck();
        mallard.performFly();
        mallard.performQuack();
        mallard.setFlyBehavior(new FlyNoWay());
        System.out.println("hack off the wings");
        mallard.performFly();
    }
}
