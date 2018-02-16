<?php 
$Prenom= $_POST["prenom"];
$mdp= $_POST["mdp"];

$con=mysqli_connect("localhost","root","root","thomas");
$result = mysqli_query($con, "SELECT id FROM users WHERE Prenom = '".$Prenom."'");
$row = mysqli_fetch_array($result, MYSQLI_ASSOC);

foreach ($row as &$value) {

}

?>