package headFirst.Decorator;

public class HouseBlend extends Beverage {
    public HouseBlend() {
        description = "House Blend Tea";
    }

    public double cost() {
        return .89;
    }
}
