package headFirst.Proxy;

import java.rmi.Naming;

public class MyRemoteClient {
    public static void main(String[] args) {
        MyRemoteClient myRemoteClient = new MyRemoteClient();
        myRemoteClient.go();

//        new MyRemoteClient().go();
    }

    public void go() {
        try {
            MyRemote service = (MyRemote) Naming.lookup("rmi://127.0.0.1/RemoteHello");
            String s = service.sayHello();
            System.out.println(s);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
