public class RunnableDemo {
    static class MyRunnable implements Runnable {
        private int id;
        public MyRunnable(int id) { this.id = id; }

        public void run() {
            for (int i = 1; i <= 3; i++) {
                System.out.println("Runnable-" + id + " step " + i);
                try { Thread.sleep(100); } catch (InterruptedException e) {}
            }
            System.out.println("Runnable-" + id + " finished");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Main: starting runnables");
        Thread t1 = new Thread(new MyRunnable(1));
        Thread t2 = new Thread(new MyRunnable(2));
        Thread t3 = new Thread(new MyRunnable(3));

        t1.start(); t2.start(); t3.start();
        t1.join(); t2.join(); t3.join();

        System.out.println("Main: all runnables done");
    }
}
