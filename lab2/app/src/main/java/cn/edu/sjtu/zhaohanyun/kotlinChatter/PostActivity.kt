package cn.edu.sjtu.zhaohanyun.kotlinChatter

import Chatt
import ChattStore.postChatt

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.Menu
import android.view.Menu.FIRST
import android.view.Menu.NONE
import android.view.MenuItem
import cn.edu.sjtu.zhaohanyun.kotlinChatter.databinding.ActivityPostBinding

class PostActivity : AppCompatActivity() {
//    override fun onCreate(savedInstanceState: Bundle?) {
//        super.onCreate(savedInstanceState)
//        setContentView(R.layout.activity_post)
//    }
    private lateinit var view: ActivityPostBinding
    private var enableSend = true

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        view = ActivityPostBinding.inflate(layoutInflater)
        setContentView(view.root)
    }

    override fun onPrepareOptionsMenu(menu: Menu?): Boolean {
        menu?.apply {
            add(NONE, FIRST, NONE, getString(R.string.send))
            getItem(0).setIcon(android.R.drawable.ic_menu_send).setEnabled(enableSend)
                .setShowAsAction(MenuItem.SHOW_AS_ACTION_ALWAYS)
        }
        return super.onPrepareOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == FIRST) {
            enableSend = false
            invalidateOptionsMenu()
            submitChatt()
        }
        return super.onOptionsItemSelected(item)
    }

    fun submitChatt() {
        val chatt = Chatt(username = view.usernameTextView.text.toString(),
            message = view.messageTextView.text.toString())

        postChatt(applicationContext, chatt)
        finish()
    }
}