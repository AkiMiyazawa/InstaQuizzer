package csm117.clicker;

import android.os.AsyncTask;
import android.util.Log;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class ConnectionTask extends AsyncTask<String, Void, Void> {
    protected Void doInBackground(String... answer) {
        try {
            Socket socket = new Socket(QuestionActivity.ip, Integer.parseInt(QuestionActivity.port));
            if (socket.isConnected()) {
                PrintWriter out = new PrintWriter(
                        new BufferedWriter(
                                new OutputStreamWriter(
                                        socket.getOutputStream())), true);
                out.println("{\"user_id\":" +QuestionActivity.name + ",\"answer\":\"" + answer[0]+ "\"}");
                out.close();
                socket.close();
            } else {
                Log.i("QuestionActivity", "Issue connecting");
            }
        } catch (UnknownHostException e) {
            Log.e("QuestionActivity", "Issue connecting", e);
        } catch (IOException e) {
            Log.e("QuestionActivity", "Issue connecting", e);
        } catch (NumberFormatException e) {
            Log.e("QuestionActivity", "Invalid port number", e);
        }
        return null;
    }
}
