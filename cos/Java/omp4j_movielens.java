//import System.out;
import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;

public class multi_movielens {
  public int user_size;
  public int item_size;
  public String file_path;

  public int u_id;
  public int i_id;
  public double rating;
  public int timestamp;

  public  multi_movielens(){
    this.user_size = 943;
    this.item_size = 1682;
    this.file_path = "ml-100k/u.data";
  }

  public double cos_sim(double v1[], double v2[]){
    double[] v1_ = v1;
    double[] v2_ = v2;

    return np_dot(v1_, v2_) / (linalg_norm(v1_) * linalg_norm(v2_));
  }

  public double np_dot(double[] v1, double[] v2){
    double dot = 0.;
    for(int i = 0; i < v1.length; i ++){
      dot = dot + v1[i] * v2[i];
    }
    return dot;
  }

  public double linalg_norm(double[] v1){
    double pow = 0.;
    for(int i = 0; i < v1.length; i++){
      pow = pow + Math.pow(v1[i], v1.length);
    }
    return Math.pow(pow, 1/v1.length);
  }

  public void distinguish_info(String line){
    String[] splitedData = line.split("[\\s]+");
    u_id      = Integer.parseInt(splitedData[0]) - 1;
    i_id      = Integer.parseInt(splitedData[1]) - 1;
    rating    = Double.parseDouble(splitedData[2]);
    timestamp = Integer.parseInt(splitedData[3]);

  }
  public void calc_cossim(int target_u_id, double[] target_user_eval){
    double[][] sim_table = new double[item_size][item_size];
    double[] user_eval = new double[item_size];
    for(int u_id = 0; u_id < user_size; u_id++){
      sim_table[target_u_id][u_id] = cos_sim(target_user_eval, user_eval);
    }
  }

  public String erapsed_time(long time){
    double e_time = (double)time;
    //ns to s
    e_time = e_time / Math.pow(10, 9);
    return "総時間 : " + e_time + " s";
  }
  public void run(){
    try{
      File f = new File(file_path);
      if(f.exists()){
        String line;
        FileReader fReader = new FileReader(f);
        BufferedReader bReader = new BufferedReader(fReader);

        double[][] eval_table = new double[user_size][item_size];

        long start = System.nanoTime();
        while((line = bReader.readLine()) != null){
          distinguish_info(line);
          eval_table[u_id][i_id] = rating;
        }
        fReader.close();

        //int target_u_id;
        double[] target_user_eval = new double[user_size];
        // omp parallel for threadNum(4)
        for(int target_u_id = 0; target_u_id < u_id; target_u_id++){
          target_user_eval = eval_table[target_u_id];
          calc_cossim(target_u_id, target_user_eval);
        }
        long time = System.nanoTime() - start;

        System.out.println(erapsed_time(time));
    } else {
      System.out.println("File not found.");
    }
  } catch (IOException e) {
    e.printStackTrace();
  }
}

  public static void main(String args[]){
    System.out.println("マルチスレッド(スレッド数4)");
    multi_movielens m = new multi_movielens();
    m.run();
  }
}
