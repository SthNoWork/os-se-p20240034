import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class PoolDemo {
    static class Task implements Runnable {
        private int id;
        public Task(int id) { this.id = id; }

        public void run() {
            System.out.println("Task-" + id + " running on " + Thread.currentThread().getName());
            try { Thread.sleep(200); } catch (InterruptedException e) {}
            System.out.println("Task-" + id + " done");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Main: creating thread pool (size=2)");
        ExecutorService pool = Executors.newFixedThreadPool(2);

        for (int i = 1; i <= 5; i++) {
            pool.submit(new Task(i));
        }

        pool.shutdown();
        while (!pool.isTerminated()) { Thread.sleep(100); }
        System.out.println("Main: all tasks completed");
    }
}
