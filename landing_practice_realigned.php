<?php
/**
 * Template Name: Landing Practice Page (Realigned)
 * 
 * Above-the-Fold Content Realignment - REVISED
 * 
 * Changes from original:
 * - Moved practice_types_of_cases_section UP after banner_badge_section
 * - This places main body content above the about/lawyer sections
 * - Improves content visibility and SEO performance
 * 
 * @package VAS Theme
 */

get_header(); 
?>

<?php 
// ==============================================
// SECTION 1: Hero Banner
// ==============================================
get_template_part('template-parts/practice_banner_section'); 
?>

<?php 
// ==============================================
// SECTION 2: Trust Badges
// ==============================================
get_template_part('template-parts/banner_badge_section'); 
?>

<?php 
// ==============================================
// SECTION 3: Cases Content (MOVED UP)
// Main body content - now appears above the fold
// This was previously after lawyer_areas_section
// ==============================================
get_template_part('template-parts/practice_types_of_cases_section'); 
?>

<?php 
// ==============================================
// SECTION 4: About Section (Video + CTA)
// ==============================================
get_template_part('template-parts/practice_about_areas_section'); 
?>

<?php 
// ==============================================
// SECTION 5: Lawyer/Team Section
// ==============================================
get_template_part('template-parts/lawyer_areas_section'); 
?>

<?php 
// ==============================================
// SECTION 6: Video Testimonials
// ==============================================
get_template_part('template-parts/home_video_areas_section'); 
?>

<?php 
// ==============================================
// SECTION 7: Text Testimonials
// ==============================================
get_template_part('template-parts/testimonials_section'); 
?>

<?php 
// ==============================================
// SECTION 8: FAQs
// ==============================================
get_template_part('template-parts/practice_faq_section'); 
?>

<?php 
// ==============================================
// SECTION 9: Popups
// ==============================================
get_template_part('template-parts/practice_popup_section');
get_template_part('template-parts/multi_popup_section'); 
?>

<?php get_footer(); ?>
