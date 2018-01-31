package headFirst.Collection;

import java.util.ArrayList;
import java.util.Iterator;

public class Waitress {
//    Menu pancakeHouseMenu;
//    Menu dinerMenu;
//    Menu coffeeMenu;
//
//    public Waitress(Menu pancakeHouseMenu, Menu dinerMenu, Menu coffeeMenu) {
//        this.pancakeHouseMenu = pancakeHouseMenu;
//        this.dinerMenu = dinerMenu;
//        this.coffeeMenu = coffeeMenu;
//    }
//
//    public void printMenu() {
//        Iterator pancakeIterator = pancakeHouseMenu.createIterator();
//        Iterator dinerIterator = dinerMenu.createIterator();
//        Iterator coffeeIterator = coffeeMenu.createIterator();
//
//        System.out.println("MENU\n----\nBREAKFAST");
//        printMenu(pancakeIterator);
//        System.out.println("\nLUNCH");
//        printMenu(dinerIterator);
//        System.out.println("\nDINNER");
//        printMenu(coffeeIterator);
//
//    }
//
//    public void printMenu(Iterator iterator) {
//        while (iterator.hasNext()) {
//            MenuItem menuItem = (MenuItem) iterator.next();
//
//            System.out.print(menuItem.getName() + ", ");
//            System.out.print(menuItem.getPrice() + "---");
//            System.out.println(menuItem.getDescription());
//        }
//    }

//    ArrayList menus;
//
//    public Waitress(ArrayList menus) {
//        this.menus = menus;
//    }
//
//    public void printMenu() {
//        Iterator menuIterator = menus.iterator();
//        while (menuIterator.hasNext()) {
//            Menu menu = (Menu) menuIterator.next();
//            printMenu(menu.createIterator());
//        }
//    }
//
//    void printMenu(Iterator iterator) {
//        while (iterator.hasNext()) {
//            MenuItem menuItem = (MenuItem) iterator.next();
//
//            System.out.print(menuItem.getName() + ", ");
//            System.out.print(menuItem.getPrice() + "---");
//            System.out.println(menuItem.getDescription());
//        }
//    }

    MenuComponent allMenus;
    public Waitress(MenuComponent allMenus) {
        this.allMenus = allMenus;
    }

    public void printMenu() {
//        Iterator iterator = allMenus.createIterator();
//        while (iterator.hasNext()) {
//            MenuComponent menuComponent = (MenuComponent) iterator.next();
//            menuComponent.print();
//        }
        allMenus.print();
    }

    public void printVegetarianMenu() {
        Iterator iterator = allMenus.createIterator();
        System.out.println("\nVegetarian Menu\n----");
        while (iterator.hasNext()) {
            MenuComponent menuComponent = (MenuComponent) iterator.next();
            try {
                if (menuComponent.isVegetarian()) {
                    menuComponent.print();
                }
            } catch (UnsupportedOperationException e) {}
        }
    }
}
