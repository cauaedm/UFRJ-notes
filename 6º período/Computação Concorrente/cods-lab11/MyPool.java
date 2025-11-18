/* Disciplina: Programacao Concorrente */
/* Prof.: Silvana Rossetto */
/* Laboratório: 11 */
/* Codigo: Criando um pool de threads em Java */

import java.util.LinkedList;

//-------------------------------------------------------------------------------
//!!! Documentar essa classe !!!
class FilaTarefas {
    // Número de threads
    private final int nThreads;

    // Array com a pool de threads
    private final MyPoolThreads[] threads;

    // Fila de tarefas (Runnable)
    private final LinkedList<Runnable> queue;

    // Flag volátil que sinaliza se o pool de threads deve ser encerrado
    private boolean shutdown;

    // Método de inicialização
    // Cria as threads, adiciona na fila e já inicia as threads

    public FilaTarefas(int nThreads) {
        this.shutdown = false;
        this.nThreads = nThreads;
        queue = new LinkedList<Runnable>();
        threads = new MyPoolThreads[nThreads];
        for (int i=0; i<nThreads; i++) {
            threads[i] = new MyPoolThreads();

            //A JVM agenda essa nova thread para rodar
            threads[i].start();
        }
    }

    //
    public void execute(Runnable r) {
        synchronized(queue) {
            if (this.shutdown) return;
            queue.addLast(r);
            queue.notify();
        }
    }
    /**/
    public void shutdown() {
        synchronized(queue) {
            this.shutdown=true;
            queue.notifyAll();
        }
        for (int i=0; i<nThreads; i++) {
          try { threads[i].join(); } catch (InterruptedException e) { return; }
        }
    }

    /**/
    private class MyPoolThreads extends Thread {
       public void run() {
         Runnable r;
         while (true) {
           synchronized(queue) {
             while (queue.isEmpty() && (!shutdown)) {
               try { queue.wait(); }
               catch (InterruptedException ignored){}
             }
             if (queue.isEmpty()) return;
             r = (Runnable) queue.removeFirst();
           }
           try { r.run(); }
           catch (RuntimeException e) {}
         }
       }
    }
}
//-------------------------------------------------------------------------------

//--PASSO 1: cria uma classe que implementa a interface Runnable
class Hello implements Runnable {
   String msg;
   public Hello(String m) { msg = m; }

   //--metodo executado pela thread
   public void run() {
      System.out.println(msg);
   }
}

class Primo implements Runnable {

    // 1. Variável de membro para guardar o número
    private int numero;

    // 2. Este é o CONSTRUTOR correto
    // Sem tipo de retorno (nem int, nem void)
    public Primo(int n) {
        this.numero = n;
    }

    // 3. O método run() agora faz o trabalho
    public void run() {
        if (ehPrimo(this.numero)) {
            System.out.println(this.numero + " eh primo.");
        } else {
            // Opcional: imprimir se não for primo
            System.out.println(this.numero + " nao eh primo.");
        }
    }

    // 4. Sua lógica de "ehPrimo" movida para um método auxiliar
    //    (e com a correção para Math.sqrt())
    private boolean ehPrimo(int n) {
        if (n <= 1) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;

        // Use Math.sqrt() e a condição correta é <=
        for (int i = 3; i <= Math.sqrt(n); i += 2) {
            if (n % i == 0) return false;
        }
        return true;
    }
}

//Classe da aplicação (método main)
class MyPool {
    private static final int NTHREADS = 12;

    public static void main (String[] args) {
        //--PASSO 2: cria o pool de threads
        FilaTarefas pool = new FilaTarefas(NTHREADS);

        System.out.println("Iniciando pool com " + NTHREADS + " threads.");
        System.out.println("Testando numeros de 0 a 24...");

        //--PASSO 3: dispara a execução dos objetos runnable usando o pool de threads
        for (int i = 0; i < 25; i++) {
            // A linha abaixo agora funciona, pois o construtor Primo(int) existe
            Runnable primo = new Primo(i);
            pool.execute(primo);
        }

        //--PASSO 4: esperar pelo termino das threads
        pool.shutdown();
        System.out.println("Terminou");
    }
}