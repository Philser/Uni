<?php
	if($_POST["index"]){
      $fh = fopen('index.log','a');
	  ftruncate($fh, 0);
      fwrite($fh, round($_POST["index"]));
      flock($fh, LOCK_UN);
      fclose($fh);
	}else{
	  echo '{"index": "'.file_get_contents('./index.log', true).'"}';
	}
?>