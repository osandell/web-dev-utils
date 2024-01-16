<?php
/*
Plugin Name: Archive First 10 Posts and Pages
Description: Automatically archives the first 10 published posts and pages by changing their status to 'draft'.
Version: 1.0
Author: Your Name
*/
add_action('wp_loaded', 'archive_first_ten_posts_pages');

function archive_first_ten_posts_pages()
{
  $args = array(
    'post_type' => array('post', 'page'),
    'post_status' => 'publish',
    'posts_per_page' => 10, // Limit to first 10 posts/pages
    'orderby' => 'date', // Order by date
    'order' => 'DESC' // Start with the most recent
  );

  $all_posts_pages = get_posts($args);

  foreach ($all_posts_pages as $post_page) {
    wp_update_post(array(
      'ID' => $post_page->ID,
      'post_status' => 'draft'
    ));
    error_log('Post/Page Archived: ' . $post_page->ID . ' - ' . $post_page->post_title);
  }
}
