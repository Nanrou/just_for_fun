package headFirst.Singleton;

public class ChocolateBoiler2 {
    private static ChocolateBoiler2 uniqueInstance = new ChocolateBoiler2();

    private ChocolateBoiler2() {}

    public static synchronized ChocolateBoiler2 getUniqueInstance() {
        return uniqueInstance;
    }

}
