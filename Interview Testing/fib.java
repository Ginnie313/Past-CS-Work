class fib_sequence{
  static int fib(int n){
    if (n < 0){
      System.out.println("You have entered an invalid number");
      return -1;
    }
    if(n <= 1){
      return n;
    }
    else{
      return fib(n-1) + fib(n-2);
    }
  }
  static void fibonacci_list(int n){
    for (int i = 0; i < n; i++){
      System.out.println(fib(i));
    }
  }
  public static void main (String args[]){
    int n = 9;
    System.out.println(fib(n));
    fibonacci_list(n);
  }
}
