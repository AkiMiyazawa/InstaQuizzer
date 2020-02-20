package csm117.clicker;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class QuestionActivity extends AppCompatActivity {
    private String answer;
    public static String name;
    public static String ip;
    public static String port;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_question);

        // Get the Intent that started this activity and extract the strings
        Intent intent = getIntent();
        name = intent.getStringExtra(HomeActivity.NAME_MESSAGE);
        ip = intent.getStringExtra(HomeActivity.IP_MESSAGE);
        port = intent.getStringExtra(HomeActivity.PORT_MESSAGE);
    }

    public void onA(View view) {
        sendAndClose("A");
    }

    public void onB(View view) {
        sendAndClose("B");
    }

    public void onC(View view) {
        sendAndClose("C");
    }

    public void onD(View view) {
        sendAndClose("D");
    }

    public void onE(View view) {
        sendAndClose("E");
    }

    public void onF(View view) { sendAndClose("F"); }

    public void sendAndClose(String answer) {
        new ConnectionTask().execute(answer);
    }
}
