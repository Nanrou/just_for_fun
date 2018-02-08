package headFirst.Compound.Duck;

public class QuackCounter implements Quackable {
    Quackable duck;
    static int numberOfQuack;

    public QuackCounter(Quackable duck) {
        this.duck = duck;
    }

    @Override
    public void quack() {
        duck.quack();
        numberOfQuack++;
    }

    public static int getNumberOfQuack() {
        return numberOfQuack;
    }

    @Override
    public void registerObserver(Observer observer) {
        duck.registerObserver(observer);  // 这只是去调用鸭子本身的方法
    }

    @Override
    public void notifyObserver() {
        duck.notifyObserver();
    }
}
