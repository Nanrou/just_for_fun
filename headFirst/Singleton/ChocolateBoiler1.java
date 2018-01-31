package headFirst.Singleton;

public class ChocolateBoiler1 {
    private static ChocolateBoiler1 uniqueInstance;

    private ChocolateBoiler1() {}

    public static synchronized ChocolateBoiler1 getUniqueInstance() {
        if (uniqueInstance == null) {
            uniqueInstance = new ChocolateBoiler1();
        }
        return uniqueInstance;
    }

}
