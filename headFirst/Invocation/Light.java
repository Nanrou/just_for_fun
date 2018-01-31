package headFirst.Invocation;

public class Light {
    String name;

    public Light(String name) {
        this.name = name;
    }

    public void on() {
        System.out.println(name + " Light is On");
    }

    public void off() {
        System.out.println(name + " Light is Off");
    }
}
