<?php
	$USER_NAME = "root"; //TODO
	$PASSWORD = "!vsruser!";  //TODO
	$DATABASE_NAME = "uebung3"; //TODO
        
        // Connect to DB
	mysql_connect("localhost",$USER_NAME,$PASSWORD) or die("Error: Could not connect to database");
	mysql_select_db($DATABASE_NAME);
	
	
	// Execute query 
	//$name = "Max";
        $sql = "SELECT * FROM personen WHERE name = '"; //TODO

        //$result = mysql_query($sql.$name."'");
        //$error = mysql_error();

        // Store results
        //while($row = mysql_fetch_array($result)) {
        // 	$data[] = $row;
        //}		
?>
<html>
<head>
</head>
<body>
<?php if(!empty($error))
	echo "<p style='color:red'>$error</p>";
?>
<p>Please enter the name:</p>
<form action="<?=$_SERVER['PHP_SELF']?>" method="POST">
<input type="input" name="name" value="" />
<br/>
<input type="submit" name="submit" value="Send" />
</form>
<?php
	if(isset($_POST['submit'])){
	
		$name = $_POST['name'];
		$result = mysql_query($sql.$name."'");
        	$error = mysql_error();

		// Store results
		while($row = mysql_fetch_array($result)) {
		 	$data[] = $row;
        }	

	}
	if(!empty($data)) {
		echo "<h1>Persons:</h1><table border='1'><tr><th>Id</th><th>Firstname</th><th>Age</th></tr>";
		foreach($data as $row) {
			echo "<tr><td>".$row["id"]."</td>";
			echo "<td>".$row["name"]."</td>";
			echo "<td>".$row["age"]."</td></tr>";
		}
		echo "</table>";
	}
	else
		echo "No data available";

        echo '(Query: '.$sql.$name."'".')';      
?>
</body>
</html>
