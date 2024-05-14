<h1 style="text-align:center;">JWT Authentication with httpOnly Cookies</h1>

<h3 style="color:#6A1B9A;">Technologies</h3>
<ul>
    <li>Django rest framework</li>
    <li>Ajax</li>
    <li>JWT</li>
    <li>Redis</li>
</ul>

<p>
    I have set a security stamp field(UUID) for every user in redis memory and jwt access token after logging in.
    For every request that required authentication,that security stamp will check in redis memory and also in access token and if they are not equal the client will redirect to login page.The security stamp will change after every important endpoints like changing passwords, changing roles and so on.
</p>
<p>
    Also the user's information encodes into his access token after his authorization and if the security stamp in redis and jwt are not changed,user sees his profile without any queries to database...
</p>


