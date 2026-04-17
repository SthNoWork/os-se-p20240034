public class ThreadDemo {
    static class MyThread extends Thread {
        private int id;
        public MyThread(int id) { this.id = id; }

        public void run() {
            for (int i = 1; i <= 3; i++) {
                System.out.println("Thread-" + id + " step " + i);
                try { Thread.sleep(100); } catch (InterruptedException e) {}
            }
            System.out.println("Thread-" + id + " finished");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Main: starting threads");
        MyThread t1 = new MyThread(1);
        MyThread t2 = new MyThread(2);
        MyThread t3 = new MyThread(3);

        t1.start(); t2.start(); t3.start();
        t1.join(); t2.join(); t3.join();

        System.out.println("Main: all threads done");
    }
}
