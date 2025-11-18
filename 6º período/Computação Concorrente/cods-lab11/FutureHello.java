import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import java.util.ArrayList;
import java.util.List;

class MyCallable implements Callable<Long> {
    MyCallable() {}

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

    Primo_Call(int i, int j){
        this.menorNumero = i;
        this.maiorNumero = j;
    }

    public Integer call() throws Exception{
        Integer count = this.contaPrimos(this.menorNumero, this.maiorNumero);
        System.out.println("Quantidade de primos entre "+this.menorNumero + " e " + this.maiorNumero + " e: ");
        return count;
    }

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
        }    
    }

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

public class FutureHello {
    private static final int N = 100; 
    private static final int NTHREADS = 4;

    public static void main(String[] args) {
        ExecutorService executor = Executors.newFixedThreadPool(NTHREADS);
        
        List<Future<Integer>> list = new ArrayList<Future<Integer>>();
        
        int chunkSize = N / NTHREADS; 
        int inicio = 1;
        int fim = 0;

        for (int i = 0; i < NTHREADS; i++) {
            fim = inicio + chunkSize - 1;
            
            if (i == NTHREADS - 1) {
                fim = N;
            }

            Callable<Integer> worker = new Primo_Call(inicio, fim);
            Future<Integer> submit = executor.submit(worker);
            list.add(submit);

            inicio = fim + 1;
        }

        Integer sum = 0;
        System.out.println("Processando...");
        
        for (Future<Integer> future : list) {
            try {
                sum += future.get(); 
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }

        System.out.println("Total de primos entre 1 e " + N + ": " + sum);
        executor.shutdown();
    }
}
