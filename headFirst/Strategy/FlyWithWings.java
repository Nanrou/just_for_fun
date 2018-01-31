package headFirst.Strategy;

public class FlyWithWings implements FlyBehavior {
    @Override
    public void fly() {
        System.out.println("I am flying! With my wings~");
    }
}
