<?php 

require_once('modules/credit.php');
require_once('include/menu.php');
require_once('include/header.php');

?>
			<? print_menu('credits'); ?>	
			<br/><br/><br/><br/>

<script type="text/javascript">
	$(function() {
		$('#add_credit').click(function() {
			a=$('#amount').val()
			n=($('#callerid1').val() == $('#callerid2').val() && a>0) ? $('#callerid1').val() : false
			if (n) { return confirm('$'+a+' --> '+n+'?') }
		});
	});
</script>


			<?php


function print_form($post_data,$errors) {

	$callerid1 = ($_POST['callerid1'] != '') ? $_POST['callerid1'] : '';
	$callerid2 = ($_POST['callerid2'] != '') ? $_POST['callerid2'] : '';
	$amount = ($_POST['amount'] != '') ? $_POST['amount'] : '';

?>

			<div id="stylized" class="myform">
				<form id="form" name="form" method="post" action="credit.php">
				<h1><?= _("Add Credit") ?></h1><br/>
				
				<span style='color: red; font-size: 12px;'><?= $errors ?></span><br/>
				<label><?= _("Subscriber number") ?>
				<span class="small"><?= _("Subscriber number") ?></span>
				</label>
				<input type="text" name="callerid1" id="callerid1" value="<?=$callerid1?>"/>

				<label><?= _("Subscriber number") ?>
				<span class="small"><?= _("Repeat Subscriber Number") ?></span>
				</label>
				<input type="text" name="callerid2" id="callerid2" value="<?=$callerid2?>"/>

				<label><?= _("Amount") ?>
				<span class="small"><?= _("Amount to add") ?></span>
				</label>
				<input type="text" name="amount" id="amount" value="<?=$amount?>"/><br/>
			
				<button type="submit" id="add_credit" name="add_credit"><?= _("Add") ?></button>
				<div class="spacer"></div>
				</form>
			</div>
<?
}	

				$error_txt = "";
				// errors check
				if (isset($_POST['add_credit'])) {
					// form pressed verify if any data is missing
					$callerid1 = $_POST['callerid1'];
					$callerid2 = $_POST['callerid2'];
					$amount = $_POST['amount'];

					if (strcmp($callerid1,$callerid2) != 0 ) {
						$error_txt .= _("Subscriber number do not match")."<br/>";
					}
					if ($callerid1 == "") {
						$error_txt .= _("Subscriber number")." 1 "._("is empty")."<br/>";
					}
					if ($callerid2 == "") {
						$error_txt .= _("Subscriber number")." 2 "._("is empty")."<br/>";
					}
					if ($amount == "" || $amount == 0 || !is_numeric($amount)) {
						$error_txt .= _("Invalid amount")."<br/>";
					}
				} 

				if (isset($_POST['add_credit']) && $error_txt != "") {
					print_form(1,$error_txt);
				}elseif (isset($_POST['add_credit']) && $error_txt == "") {
					// get some data out based on user input
					$callerid = $_POST['callerid1'];
					$amount = $_POST['amount'];
					echo "<center>";
					$cred = new Credit();
					try {
						$cred->add($callerid,$amount);
						echo "<img src='img/true.png' width='200' height='170' /><br/><br/>";
						echo "<span style='font-size: 20px;'>"._("Credit of")." <b>$amount</b> "._("pesos successfully added to subscriber")." <b>$callerid</b>.</span><br/><br/><br/>";
						echo "<a href='credit.php'><button class='b1'>"._("Go Back")."</button></a>";
					} catch (CreditException $e) {
						echo "<img src='img/false.png' width='200' height='170' /><br/><br/>";
						echo "<span style='font-size: 20px; color: red;'>"._("ERROR UPDATING BALANCE!")."<br/>".$e->getMessage()." </span><br/><br/><br/><br/>";
						echo "<a href='credit.php'><button class='b1'>"._("Go Back")."</button></a>";
					}
					echo "</center>";
				} else {
					print_form(0,'');
				}

			?>

		</div>
	</body>

</html>
