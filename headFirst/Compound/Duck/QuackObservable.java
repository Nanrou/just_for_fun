package headFirst.Compound.Duck;

public interface QuackObservable {
    public void registerObserver(Observer observer);
    public void notifyObserver();
}
