package headFirst.Collection;

import java.util.ArrayList;
import java.util.Iterator;

public class Menu extends MenuComponent {  // 这个接口类似标记接口，方便后面调用时接收这个共同的接口
    ArrayList menuComponents = new ArrayList();
    String name;
    String description;

    public Menu(String name, String description) {
        this.name = name;
        this.description = description;
    }

    public void add(MenuComponent menuComponent) {
        menuComponents.add(menuComponent);
    }

    public void remove(MenuComponent menuComponent) {
        menuComponents.remove(menuComponent);
    }

    @Override
    public MenuComponent getChild(int i) {
        return (MenuComponent)menuComponents.get(i);
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String getDescription() {
        return description;
    }

    @Override
    public void print() {
        System.out.print("\n" + getName());
        System.out.println(", " + getDescription());
        System.out.println("---------------------");

        Iterator iterator = menuComponents.iterator();
//        Iterator iterator = this.createIterator();
//        Iterator iterator = createIterator();
//        Iterator iterator = new CompositeIterator(this.createIterator());
        while (iterator.hasNext()) {
            MenuComponent menuComponent = (MenuComponent)iterator.next();
            menuComponent.print();
        }

//        for (Object menuComponent: menuComponents) {
//            (MenuComponent)menuComponent.print();
//        }
    }

    @Override
    public Iterator createIterator() {
        return new CompositeIterator(menuComponents.iterator());
//        return menuComponents.iterator();
    }
}
