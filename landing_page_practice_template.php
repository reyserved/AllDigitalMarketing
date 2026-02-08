<?php
/**
 * Template Name: Landing Practice
 *
 */


$spanish = get_field('spanish');
if($spanish == ""){

get_header();

$current_page_slug = basename(get_permalink());
 
 
 
if($current_page_slug == "miami-divorce-lawyer-msh" || $current_page_slug == "miami-family-law-msh" || $current_page_slug == "miami-prenup-lawyer-msh" || $current_page_slug =="miami-abogado-de-derecho-familiar"){
    get_template_part( 'template-parts/practice_banner_section_msh', 'none' );
    ?><div id="about"><?php
    get_template_part( 'template-parts/practice_about_areas_section_msh', 'none' );
    ?></div><?php
}else{
    get_template_part( 'template-parts/practice_banner_section', 'none' );
    get_template_part( 'template-parts/banner_badge_section', 'none' );
    get_template_part( 'template-parts/practice_about_areas_section', 'none' );
}

get_template_part( 'template-parts/lawyer_areas_section', 'none' );
?>
<div id="services">
    <?php
        get_template_part( 'template-parts/practice_types_of_cases_section', 'none' );
    ?>
</div>
<div id="videos">
    <?php
        get_template_part( 'template-parts/home_video_areas_section', 'none' );
    ?>
</div>
<div id="reviews">
    <?php
        get_template_part( 'template-parts/testimonials_section', 'none' );
        ?>
</div>



<?php
    
    get_template_part( 'template-parts/practice_faq_section', 'none' );
    get_template_part( 'template-parts/practice_popup_section', 'none' );
    get_template_part( 'template-parts/multi_popup_section', 'none' );
if($current_page_slug == "miami-divorce-lawyer-msh" || $current_page_slug == "miami-family-law-msh" || $current_page_slug == "miami-prenup-lawyer-msh" || $current_page_slug =="miami-abogado-de-derecho-familiar"){
?>
<div id="msh-form-container" class="container">
    <div class="row">
        <div class="col-lg-5 mx-auto col-12 py-5">
         <h4 class="text-center mt-5">Ge A Free Case Evaluation</h4>
            <div id="msh-form">
           
            <?php
				if($current_page_slug == "miami-family-law-msh"){
					echo "Family Law";
							?>
				<!-- Start Lawmatics Embedded Snippet -->
<script id="lm-embedded-script">
    !function (e, t, n, a, s, c, i) { if (!e[s]) { i = e[s] = function () { i.process ? i.process.apply(i, arguments) : i.queue.push(arguments) }, i.queue = [], i.t = 1 * new Date; var o = t.createElement(n); o.async = 1, o.src = a + "?t=" + Math.ceil(new Date / c) * c; var r = t.getElementsByTagName(n)[0]; r.parentNode.insertBefore(o, r) } }(window, document, "script", "https://navi.lawmatics.com/intake.min.js", "lm_intake", 864e5), lm_intake("7dc2ebd9-ac5c-4e4d-94db-ade69e3ca493", "msh-form");
</script>
<!-- End Lawmatics Embedded Snippet -->
				<?php
						}
						if($current_page_slug == "miami-prenup-lawyer-msh"){
							echo "Prenups";
							?>
				
<!-- Start Lawmatics Embedded Snippet -->
<script id="lm-embedded-script">
    !function(e,t,n,a,s,c,i){if(!e[s]){i=e[s]=function(){i.process?i.process.apply(i,arguments):i.queue.push(arguments)},i.queue=[],i.t=1*new Date;var o=t.createElement(n);o.async=1,o.src=a+"?t="+Math.ceil(new Date/c)*c;var r=t.getElementsByTagName(n)[0];r.parentNode.insertBefore(o,r)}}(window,document,"script","https://navi.lawmatics.com/intake.min.js","lm_intake",864e5),lm_intake("6002799f-d60a-4694-b56c-b7799825ffa8", "msh-form");
    </script>
    <!-- End Lawmatics Embedded Snippet -->
				<?php
						}
						if($current_page_slug == "miami-abogado-de-derecho-familiar"){
							echo "Spanish";
							?>
				<!-- Start Lawmatics Embedded Snippet -->
<script id="lm-embedded-script">
    !function (e, t, n, a, s, c, i) { if (!e[s]) { i = e[s] = function () { i.process ? i.process.apply(i, arguments) : i.queue.push(arguments) }, i.queue = [], i.t = 1 * new Date; var o = t.createElement(n); o.async = 1, o.src = a + "?t=" + Math.ceil(new Date / c) * c; var r = t.getElementsByTagName(n)[0]; r.parentNode.insertBefore(o, r) } }(window, document, "script", "https://navi.lawmatics.com/intake.min.js", "lm_intake", 864e5), lm_intake("6613e172-b112-4390-aa1c-9aaf0350d095","msh-form");
</script>
<!-- End Lawmatics Embedded Snippet -->
				<?php
						}
				?>

 
            </div>
        </div>
    </div>
</div>
<div class="msh-cta">
<?php
    $landingPhone="";
    if($current_page_slug == "miami-divorce-lawyer-msh")
    {
    $landingPhone="305-930-8699";
    }
    if($current_page_slug == "miami-family-law-msh")
    {
        $landingPhone="305-930-8699";
    }
    if($current_page_slug == "miami-prenup-lawyer-msh")
    {
        $landingPhone="(786) 756-6997";
    }
 ?>
    <a href="tel:<?php echo $landingPhone;  ?>">Call Now <?php echo $landingPhone;  ?></a>
</div>
<?php
}
get_footer();  
}else{
get_header('es');
$current_page_slug = basename(get_permalink());
if($current_page_slug =="miami-abogado-de-derecho-familiar"){
    if(!wp_is_mobile()){
        get_template_part( 'template-parts/practice_banner_section_es_msh', 'none' );   
    }
    ?><div id="about"><?php
        get_template_part( 'template-parts/practice_about_areas_section_es_msh', 'none' ); 
    ?></div><?php
}else{
    get_template_part( 'template-parts/practice_banner_section_es', 'none' );
    get_template_part( 'template-parts/banner_badge_section', 'none' );    
    get_template_part( 'template-parts/practice_about_areas_section_es', 'none' );
}
get_template_part( 'template-parts/lawyer_areas_section_es', 'none' );
?><div id="services"><?php
get_template_part( 'template-parts/practice_types_of_cases_section_es', 'none' );
?></div><?php
get_template_part( 'template-parts/home_video_areas_section_es', 'none' );
?><div id="reviews"><?php
get_template_part( 'template-parts/testimonials_section_es', 'none' );
?></div> 



<?php

get_template_part( 'template-parts/practice_faq_section', 'none' );
get_template_part( 'template-parts/practice_popup_section', 'none' );
get_template_part( 'template-parts/multi_popup_section', 'none' );
if($current_page_slug =="miami-abogado-de-derecho-familiar"){
?>
<div id="msh-form-container" class="container">
    <div class="row">
        <div class="col-lg-9 mx-auto col-12 py-5">
         <h4 class="text-center mt-5">SOLICITE SU EVALUACIÓN<br>DE CASO GRATUITA</h4>
            <div id="msh-form">
           
           <?php
				if($current_page_slug == "miami-family-law-msh"){
					 
							?>
				<!-- Start Lawmatics Embedded Snippet -->
<script id="lm-embedded-script">
    !function (e, t, n, a, s, c, i) { if (!e[s]) { i = e[s] = function () { i.process ? i.process.apply(i, arguments) : i.queue.push(arguments) }, i.queue = [], i.t = 1 * new Date; var o = t.createElement(n); o.async = 1, o.src = a + "?t=" + Math.ceil(new Date / c) * c; var r = t.getElementsByTagName(n)[0]; r.parentNode.insertBefore(o, r) } }(window, document, "script", "https://navi.lawmatics.com/intake.min.js", "lm_intake", 864e5), lm_intake("7dc2ebd9-ac5c-4e4d-94db-ade69e3ca493", "msh-form");
</script>
<!-- End Lawmatics Embedded Snippet -->
				<?php
						}
						if($current_page_slug == "miami-prenup-lawyer-msh"){
							 
							?>
				
<!-- Start Lawmatics Embedded Snippet -->
<script id="lm-embedded-script">
    !function(e,t,n,a,s,c,i){if(!e[s]){i=e[s]=function(){i.process?i.process.apply(i,arguments):i.queue.push(arguments)},i.queue=[],i.t=1*new Date;var o=t.createElement(n);o.async=1,o.src=a+"?t="+Math.ceil(new Date/c)*c;var r=t.getElementsByTagName(n)[0];r.parentNode.insertBefore(o,r)}}(window,document,"script","https://navi.lawmatics.com/intake.min.js","lm_intake",864e5),lm_intake("6002799f-d60a-4694-b56c-b7799825ffa8", "msh-form");
    </script>
    <!-- End Lawmatics Embedded Snippet -->
				<?php
						}
						if($current_page_slug == "miami-abogado-de-derecho-familiar"){
							 
							?>
				<!-- Start Lawmatics Embedded Snippet -->
<script id="lm-embedded-script">
    !function (e, t, n, a, s, c, i) { if (!e[s]) { i = e[s] = function () { i.process ? i.process.apply(i, arguments) : i.queue.push(arguments) }, i.queue = [], i.t = 1 * new Date; var o = t.createElement(n); o.async = 1, o.src = a + "?t=" + Math.ceil(new Date / c) * c; var r = t.getElementsByTagName(n)[0]; r.parentNode.insertBefore(o, r) } }(window, document, "script", "https://navi.lawmatics.com/intake.min.js", "lm_intake", 864e5), lm_intake("6613e172-b112-4390-aa1c-9aaf0350d095","msh-form");
</script>
<!-- End Lawmatics Embedded Snippet -->
				<?php
						}
				?>

 
            </div>
        </div>
    </div>
</div>
<div class="msh-cta">
<?php
    $landingPhone="";
    if($current_page_slug == "miami-abogado-de-derecho-familiar")
    {
    	$landingPhone="(786) 705-8790";
    }
 ?>
    <a href="tel:<?php echo $landingPhone;  ?>">Llámanos Ahora <?php echo $landingPhone;  ?></a>
</div>
<?php
}
get_footer('es');
}?>