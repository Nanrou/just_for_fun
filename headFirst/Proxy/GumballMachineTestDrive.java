package headFirst.Proxy;

import headFirst.Proxy.Gumball.GumballMachine;

import java.rmi.Naming;

public class GumballMachineTestDrive {
    public static void main(String[] args) {
        GumballMachineRemote gumballMachine = null;
        int count = 0;

        if (args.length < 2) {
            System.out.println("GumballMachine <name> <inventory>");
            System.exit(1);
        }
        try {
            count = Integer.parseInt(args[1]);
            gumballMachine = new GumballMachine(count, args[0]);
            Naming.bind("//" + args[0] + "/gumballmichine", gumballMachine);
        } catch (Exception e) {
            e.printStackTrace();
        }

//        GumballMonitor gumballMonitor = new GumballMonitor(newGumballMachine);
//        gumballMonitor.report();
    }
}
