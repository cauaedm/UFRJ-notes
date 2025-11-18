/* Disciplina: Programacao Concorrente */
/* Prof.: Silvana Rossetto */
/* Laboratório: 11 */
/* Codigo: Exemplo de uso de futures */
/* -------------------------------------------------------------------*/

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import java.util.ArrayList;
import java.util.List;


//classe runnable
// nesse
class MyCallable implements Callable<Long> {
    //construtor
    MyCallable() {}

    //método para execução
    public Long call() throws Exception {
        long s = 0;
        for (long i=1; i<=100; i++) {
            s++;
        }
        return s;
    }
}

class Primo_Call implements Callable<Integer>{
    private int menorNumero;
    private int maiorNumero;

    //construtor
    Primo_Call(int i, int j){
        this.menorNumero = i;
        this.maiorNumero = j;
    }

    //metodo
    public Integer call() throws Exception{
        Integer count = this.contaPrimos(this.menorNumero, this.maiorNumero);
        System.out.println("Quantidade de primos entre "+this.menorNumero + " e " + this.maiorNumero + " e: ");
        return count;
    }

    // outros métodos
    public boolean ehprimo(int var1){
        if (var1 <= 1) {
            return false;
        } else if (var1 == 2) {
            return true;
        } else if (var1 % 2 == 0) {
            return false;
        } else {
            for(int var2 = 3; (double)var2 <= Math.sqrt((double)var1); var2 += 2) {
                if (var1 % var2 == 0) {
                    return false;
                }
            }

            return true;
        }    }

    public Integer contaPrimos(int i, int j){
        Integer count = 0;
        for(Integer atual=i; atual<=j; atual++){
            if (this.ehprimo(atual)){
                count = count + 1;
            }
            else{
                continue;
            }
        }
        return count;
    }
}

//classe do método main
public class FutureHello  {
    private static final int N = 13;
    private static final int NTHREADS = 3;

    public static void main(String[] args) {
        //cria um pool de threads (NTHREADS)
        ExecutorService executor = Executors.newFixedThreadPool(NTHREADS);
        //cria uma lista para armazenar referencias de chamadas assincronas

        List<Future<Integer>> list = new ArrayList<Future<Integer>>();
        int chunkSize = N / NTHREADS; // Tamanho base de cada pedaco
        int remainder = N % NTHREADS; // O que sobra da divisao

        for (int inicio = 1; inicio < N; inicio+=chunkSize) {
            Callable<Integer> worker = new Primo_Call(inicio, inicio+chunkSize-1);

            Future<Integer> submit = executor.submit(worker);
            list.add(submit);
        }

        System.out.println(list.size());
        //pode fazer outras tarefas...

        //recupera os resultados e faz o somatório final
        Integer sum = 0;
        for (Future<Integer> future : list) {
            try {
                sum += future.get(); //bloqueia se a computação nao tiver terminado
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }
        System.out.println(sum);
        executor.shutdown();
    }
}
