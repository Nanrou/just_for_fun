package headFirst.Singleton;

public class ChocolateBoiler3 {
    private volatile static ChocolateBoiler3 uniqueInstance;

    private ChocolateBoiler3() {}

    public static ChocolateBoiler3 getUniqueInstance() {
        if (uniqueInstance == null) {  // 第一次才会彻底执行这里的代码
            synchronized (ChocolateBoiler3.class) {
                if (uniqueInstance == null) {
                    uniqueInstance = new ChocolateBoiler3();
                }
            }
        }
        return uniqueInstance;
    }
}
