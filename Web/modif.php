<?php
$Prenom= $_POST["prenom"];
$mdp= $_POST["mdp"];
$Age= $_POST["age"];
$Nourriture= $_POST["Nourriture"];
$Genre= $_POST["genre"];
$Pays= $_POST["Pays"];


$con=mysqli_connect("localhost","root","root","thomas");
mysqli_query($con,
"UPDATE users SET Prenom = '".$Prenom."', Pass = '".$mdp."', Age = '".$Age."', Genre = '".$Genre."', Nourriture = '".$Nourriture."',  Pays = '".$Pays."' WHERE id = '18'");









?>