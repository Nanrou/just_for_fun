package headFirst.Proxy.Gumball;

import java.io.Serializable;

public interface State extends Serializable {

    public void insertQuarter();   // 塞钱这个动作

    public void ejectQuarter();  // 想要退钱

    public void turnCrank();  // 扭动开关

    public void dispense();  // 分发糖果
}
