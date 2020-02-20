package csm117.clicker;

import android.content.Intent;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;

public class HomeActivity extends AppCompatActivity {
    public static final String NAME_MESSAGE = "csm117.clicker.NAME_MESSAGE";
    public static final String IP_MESSAGE = "csm117.clicker.IP_MESSAGE";
    public static final String PORT_MESSAGE = "csm117.clicker.PORT_MESSAGE";

    public static Socket socket = null;
    public static DataOutputStream dataOutputStream = null;
    public static DataInputStream dataInputStream = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    /** Called when the user taps the Send button */
    public void sendMessage(View view) {

        EditText editText = (EditText) findViewById(R.id.IPTextForm);
        String ip = editText.getText().toString();

        editText = (EditText) findViewById(R.id.PortTextForm);
        String port = editText.getText().toString();

        editText = (EditText) findViewById(R.id.NameTextForm);
        String name = editText.getText().toString();

        Intent intent = new Intent(this, QuestionActivity.class);
        intent.putExtra(IP_MESSAGE, ip);
        intent.putExtra(NAME_MESSAGE, name);
        intent.putExtra(PORT_MESSAGE, port);

        startActivity(intent);
    }
}

