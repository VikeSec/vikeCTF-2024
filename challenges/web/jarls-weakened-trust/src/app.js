const express = require('express');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');


const FLAG = 'vikeCTF{134rN_Y0Ur_4160r17HM5}';
const secretKey = Math.random().toString(36).substring(2);
const PORT = 3000;


function html(inside) {
    return `
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Jarl's Weakened Trust</title>
        <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.orange.min.css"
        />
        <style>
            body { text-align: center; }
            form { display: inline-block; }
        </style>
    </head>
    <body>
        ${inside}
    </body>
</html>
`
}

const LOGGEDOUT = `
<h2>Join Today!</h2>
<form action="/join" method="POST">
    <label for="username">Username:
        <input type="text" id="username" name="username" required />
    </label>
    <label for="password">Password:
        <input type="password" id="password" name="password" required />
    </label>
    <input type="submit" value="Login">
</form>
`

const LOGGEDIN = `
<h2>Congratulations On Joining!</h2>
<p>Someone with admin permissions will approve your application within the next millenium</p>
`

const app = express();
app.use(express.json());
app.use(cookieParser());

app.get('/', (req, res) => {
    const token = req.cookies.AUTHORIZATION;
    if (token) {
        try {
            const decoded = jwt.verify(token, secretKey);
            if (decoded.admin) {
                res.send(html(FLAG));
                return
            } else {
                res.send(html(LOGGEDIN));
                return
            }
        } catch (err) {
            console.log(err)
            res.clearCookie('AUTHORIZATION');
            res.set("Error", "JWT ERROR")
            res.status(401)
        }
    }
    res.send(html(LOGGEDOUT));
}
);

app.post('/join', (req, res) => {
    const userId = Math.random().toString(36).substring(2);
    const token = jwt.sign({ userId, admin: false }, secretKey);

    res.cookie('AUTHORIZATION', token, { httpOnly: true });
    res.redirect(302, '/')
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server is running on port ${PORT}`);
});
