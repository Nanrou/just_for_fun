package headFirst.Observer;


public class StatisticsDisplay implements Observer, DisplayElement {
    private float maxTemp = 0.0f;
    private float minTemp = 200;
    private float sumTemp = 0.0f;
    private int numReadings;
    private Subject weatherData;

    public StatisticsDisplay(Subject weatherData) {
        this.weatherData = weatherData;
        this.weatherData.registerObserver(this);  // 直接就注册自身了
    }

    public void update(float temperature, float humidity, float pressure) {
        sumTemp += temperature;
        numReadings++;
        if (temperature > maxTemp) maxTemp = temperature;
        if (temperature < minTemp) minTemp = temperature;
        display();
    }

    public void display() {
        System.out.println("Avg/Max/Min temperature = " + (sumTemp / numReadings)
        + "/" + maxTemp + "/" + minTemp);
    }
}
