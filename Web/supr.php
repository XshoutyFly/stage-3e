<?php
$annuler = $_POST["annuler"];
$supprimer = $_POST["supprimer"];
if ($annuler == True){
    header("Location: index.php");
}
else {
    echo("Supprimer");
    $con=mysqli_connect("localhost","root","root","thomas");

 mysqli_query($con, "DELETE FROM users WHERE id='18'");
}