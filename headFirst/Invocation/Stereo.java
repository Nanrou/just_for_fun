package headFirst.Invocation;

public class Stereo {
    int volume;

    public void on() {
        System.out.println("Stereo is On");
    }

    public void off() {
        System.out.println("Stereo is Off");
    }

    public void setCD() {
        System.out.println("Set CD");
    }

    public void setVolume(int volume) {
        this.volume = volume;
        System.out.println("Set Volume to " + this.volume);
    }
}
