<?php 
$Prenom= $_POST["prenom"];
$mdp= $_POST["mdp"];
$Age= $_POST["age"];
$Nourriture= $_POST["Nourriture"];
$Genre= $_POST["genre"];
$Pays= $_POST["Pays"];


$con=mysqli_connect("localhost","root","root","thomas");
mysqli_query($con,"INSERT INTO users (Prenom,Pass,Age,Nourriture,Genre,Pays) VALUES ('".$Prenom."','".$mdp."',".$Age.",'".$Nourriture."','".$Genre."','".$Pays."')");

include("header.html");
?>
    <p>Prenom: <?php echo $Prenom ?></p>
    <p>Mot de passe: <?php echo $mdp ?></p>
    <p>Age: <?php echo $Age ?></p>
    <p>Sexe: <?php echo $Genre ?></p>
    <p>Nourriture: <?php echo $Nourriture ?></p>
    <p>Pays: <?php echo $Pays ?></p>
<?php
include("footer.html");
?>