depends
=======

Toggle wemo switches with an Amazon Dash button.

## Usage

Discover the MAC address of your Amazon Dash button.

<pre>
  ./depends discover
</pre>

Edit depends.conf to map Amazon Dash button MAC addresses to Wemos.

<pre>
[
 {
  "wemo name"  : "Wemo Number One",
  "button mac" : "74:75:76:78:79:80"
 },
 {
  "wemo name"  : "Wemo Number Two",
  "button mac" : "74:75:76:78:79:81"
 }
]
</pre>

Toggle configured Wemos when Amazon Dash buttons are pressed.

<pre>
  ./depends
</pre>
