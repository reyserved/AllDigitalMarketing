# Sales Xceleration Episode Highlights Implementation Guide
## Transistor.fm Podcast Player Integration

**Prepared for:** Sales Xceleration  
**Date:** January 30, 2026  
**Platform:** WordPress + Elementor  
**Podcast Host:** Transistor.fm

---

## Overview

This guide provides two implementation approaches for creating clickable Episode Highlights in your podcast page sidebar:

1. **Option 1: Ready-to-Use HTML/CSS Snippet** — Quick, manual implementation per episode
2. **Option 2: Dynamic ACF-Based Solution** — Scalable approach for all future episodes

---

# Option 1: Ready-to-Use HTML/CSS Snippet

**Best for:** Quick single-episode implementation, testing the feature

## Step 1: Open Your Episode Page in Elementor

1. Log into WordPress Admin
2. Navigate to **Posts** → Find your podcast episode post
3. Click **Edit with Elementor**

## Step 2: Create the Sidebar Layout (if not already set up)

1. If your page doesn't have a sidebar, add a **new section**
2. Choose a **two-column layout** (70/30 or 60/40)
3. The left column = main content (player + description)
4. The right column = sidebar (Subscribe buttons + Episode Highlights)

## Step 3: Add an HTML Widget

1. In the sidebar column, drag an **HTML widget** from the Elementor panel
2. Paste the following code into the HTML widget:

```html
<!-- ============================================
     EPISODE HIGHLIGHTS - TRANSISTOR.FM PLAYER
     ============================================ -->

<div class="sxl-episode-highlights">
    <h3 class="sxl-highlights-header">
        <span class="sxl-icon">🎙️</span> Episode Highlights
    </h3>
    
    <div class="sxl-highlights-wrapper">
        
        <!-- HIGHLIGHT 1: Intro -->
        <a href="#" class="sxl-highlight-item" data-time="0" data-episode="5d8a4233">
            <span class="sxl-time">(00:00)</span>
            <span class="sxl-topic">Intro</span>
        </a>
        
        <!-- HIGHLIGHT 2 -->
        <a href="#" class="sxl-highlight-item" data-time="111" data-episode="5d8a4233">
            <span class="sxl-time">(01:51)</span>
            <span class="sxl-topic">AI tools for SMBs and how to implement them</span>
        </a>
        
        <!-- HIGHLIGHT 3 -->
        <a href="#" class="sxl-highlight-item" data-time="342" data-episode="5d8a4233">
            <span class="sxl-time">(05:42)</span>
            <span class="sxl-topic">Personalization in sales with AI</span>
        </a>
        
        <!-- HIGHLIGHT 4 -->
        <a href="#" class="sxl-highlight-item" data-time="477" data-episode="5d8a4233">
            <span class="sxl-time">(07:57)</span>
            <span class="sxl-topic">Smarter targeting starts with human insight</span>
        </a>
        
        <!-- HIGHLIGHT 5 -->
        <a href="#" class="sxl-highlight-item" data-time="695" data-episode="5d8a4233">
            <span class="sxl-time">(11:35)</span>
            <span class="sxl-topic">Balancing quantity and quality in lead gen</span>
        </a>
        
        <!-- HIGHLIGHT 6 -->
        <a href="#" class="sxl-highlight-item" data-time="1206" data-episode="5d8a4233">
            <span class="sxl-time">(20:06)</span>
            <span class="sxl-topic">Hyper-personalization strategies</span>
        </a>
        
        <!-- HIGHLIGHT 7 -->
        <a href="#" class="sxl-highlight-item" data-time="1681" data-episode="5d8a4233">
            <span class="sxl-time">(28:01)</span>
            <span class="sxl-topic">Where AI can take sales in the future</span>
        </a>
        
    </div>
</div>

<!-- ============================================
     CSS STYLES
     ============================================ -->
<style>
/* Container */
.sxl-episode-highlights {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border-left: 4px solid #c2002f;
    margin-bottom: 24px;
}

/* Header */
.sxl-highlights-header {
    font-size: 18px;
    font-weight: 700;
    color: #004877;
    margin: 0 0 16px 0;
    padding-bottom: 12px;
    border-bottom: 2px solid #e9ecef;
    display: flex;
    align-items: center;
    gap: 8px;
}

.sxl-icon {
    font-size: 20px;
}

/* Wrapper */
.sxl-highlights-wrapper {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* Individual highlight item */
.sxl-highlight-item {
    display: flex;
    flex-direction: column;
    padding: 12px 14px;
    border-radius: 8px;
    text-decoration: none !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: #ffffff;
    border: 1px solid #e9ecef;
    cursor: pointer;
}

.sxl-highlight-item:hover {
    background: linear-gradient(135deg, #fff5f7 0%, #ffffff 100%);
    border-color: #c2002f;
    transform: translateX(6px);
    box-shadow: 0 4px 12px rgba(194, 0, 47, 0.15);
}

.sxl-highlight-item:active {
    transform: translateX(3px);
}

/* Timestamp */
.sxl-time {
    color: #c2002f;
    font-weight: 700;
    font-size: 13px;
    font-family: 'Monaco', 'Consolas', monospace;
    margin-bottom: 4px;
}

/* Topic description */
.sxl-topic {
    color: #333;
    font-size: 14px;
    line-height: 1.5;
    font-weight: 500;
}

.sxl-highlight-item:hover .sxl-topic {
    color: #c2002f;
}

/* Active/Playing state */
.sxl-highlight-item.is-playing {
    background: linear-gradient(135deg, #c2002f 0%, #a50028 100%);
    border-color: #c2002f;
}

.sxl-highlight-item.is-playing .sxl-time,
.sxl-highlight-item.is-playing .sxl-topic {
    color: #ffffff;
}

/* Responsive */
@media (max-width: 768px) {
    .sxl-episode-highlights {
        padding: 18px;
        margin: 16px 0;
    }
    
    .sxl-highlight-item {
        padding: 10px 12px;
    }
    
    .sxl-topic {
        font-size: 13px;
    }
}
</style>

<!-- ============================================
     JAVASCRIPT - TRANSISTOR PLAYER CONTROL
     ============================================ -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const highlights = document.querySelectorAll('.sxl-highlight-item');
    
    highlights.forEach(function(highlight) {
        highlight.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get timestamp and episode ID from data attributes
            const timeSeconds = parseInt(this.dataset.time);
            const episodeId = this.dataset.episode;
            
            // Find the Transistor iframe on the page
            const iframe = document.querySelector('iframe[src*="transistor.fm"]');
            
            if (iframe) {
                // Update the iframe src with the timestamp parameter
                const newSrc = `https://share.transistor.fm/e/${episodeId}?time=${timeSeconds}`;
                iframe.src = newSrc;
                
                // Scroll to the player
                iframe.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
                
                // Visual feedback - mark as playing
                highlights.forEach(h => h.classList.remove('is-playing'));
                this.classList.add('is-playing');
                
            } else {
                // Fallback: Open in new tab if iframe not found
                window.open(`https://share.transistor.fm/e/${episodeId}?time=${timeSeconds}`, '_blank');
            }
        });
    });
});
</script>
```

## Step 4: Customize for Your Episode

For each episode, you'll need to update:

1. **Episode ID** - Replace `5d8a4233` with the Transistor episode ID
   - Find this in your Transistor dashboard or the embed URL
   
2. **Timestamps** - Update the `data-time` values (in seconds) and display times
   - Use this formula: `(Minutes × 60) + Seconds = Total Seconds`
   - Example: 5:42 = (5 × 60) + 42 = 342 seconds

3. **Topic descriptions** - Update the text in each `<span class="sxl-topic">`

### Timestamp Conversion Reference:

| Display Time | Formula | Seconds |
|-------------|---------|---------|
| 00:00 | (0×60)+0 | 0 |
| 01:51 | (1×60)+51 | 111 |
| 05:42 | (5×60)+42 | 342 |
| 07:57 | (7×60)+57 | 477 |
| 11:35 | (11×60)+35 | 695 |
| 20:06 | (20×60)+6 | 1206 |
| 28:01 | (28×60)+1 | 1681 |
| 33:03 | (33×60)+3 | 1983 |

## Step 5: Save and Test

1. Click **Update** to save the Elementor page
2. Preview the page
3. Click on a timestamp - it should:
   - Reload the Transistor player at that timestamp
   - Scroll the player into view
   - Highlight the selected timestamp

---

# Option 2: Dynamic ACF-Based Solution

**Best for:** Ongoing podcast episodes, content team management, scalability

## Prerequisites

- **Advanced Custom Fields (ACF)** plugin installed (free version works)
- Basic familiarity with WordPress custom fields

---

## Step 1: Install and Activate ACF

1. Go to **Plugins** → **Add New**
2. Search for "Advanced Custom Fields"
3. Install and activate **Advanced Custom Fields** by WP Engine

---

## Step 2: Create the Field Group

1. Go to **ACF** → **Field Groups** → **Add New**
2. Title: `Podcast Episode Highlights`
3. Add the following fields:

### Field 1: Transistor Episode ID
| Setting | Value |
|---------|-------|
| Field Label | Transistor Episode ID |
| Field Name | `transistor_episode_id` |
| Field Type | Text |
| Instructions | Enter the Transistor episode ID (e.g., 5d8a4233). Find this in your Transistor dashboard. |
| Required | Yes |

### Field 2: Episode Highlights (Repeater)
| Setting | Value |
|---------|-------|
| Field Label | Episode Highlights |
| Field Name | `episode_highlights` |
| Field Type | Repeater |
| Instructions | Add timestamps and descriptions for each highlight |
| Minimum Rows | 1 |
| Maximum Rows | 15 |
| Layout | Table |

**Sub-fields within the Repeater:**

#### Sub-field 2a: Timestamp Display
| Setting | Value |
|---------|-------|
| Field Label | Timestamp Display |
| Field Name | `timestamp_display` |
| Field Type | Text |
| Instructions | Format: MM:SS (e.g., 01:51) |
| Placeholder | 00:00 |

#### Sub-field 2b: Timestamp Seconds
| Setting | Value |
|---------|-------|
| Field Label | Timestamp (Seconds) |
| Field Name | `timestamp_seconds` |
| Field Type | Number |
| Instructions | Time in seconds. Formula: (Minutes × 60) + Seconds |
| Minimum Value | 0 |

#### Sub-field 2c: Highlight Title
| Setting | Value |
|---------|-------|
| Field Label | Highlight Title |
| Field Name | `highlight_title` |
| Field Type | Text |
| Instructions | Brief description of this segment |
| Character Limit | 100 |

---

## Step 3: Set Location Rules

Under **Location** settings:
- Show this field group if: **Post Type** is equal to **Post**
- (Optional) Add condition: **Post Category** is equal to **Podcast**

Click **Publish** to save the field group.

---

## Step 4: Create a Template Part for the Highlights

Create a new file in your child theme: `template-parts/podcast-highlights.php`

```php
<?php
/**
 * Template Part: Podcast Episode Highlights
 * Displays clickable timestamps for Transistor.fm podcast episodes
 */

// Get the ACF fields
$episode_id = get_field('transistor_episode_id');
$highlights = get_field('episode_highlights');

// Only display if we have data
if (!$episode_id || !$highlights) {
    return;
}
?>

<div class="sxl-episode-highlights" data-episode-id="<?php echo esc_attr($episode_id); ?>">
    <h3 class="sxl-highlights-header">
        <span class="sxl-icon">🎙️</span> Episode Highlights
    </h3>
    
    <div class="sxl-highlights-wrapper">
        <?php foreach ($highlights as $index => $highlight) : ?>
            <a href="#" 
               class="sxl-highlight-item" 
               data-time="<?php echo esc_attr($highlight['timestamp_seconds']); ?>" 
               data-episode="<?php echo esc_attr($episode_id); ?>">
                <span class="sxl-time">(<?php echo esc_html($highlight['timestamp_display']); ?>)</span>
                <span class="sxl-topic"><?php echo esc_html($highlight['highlight_title']); ?></span>
            </a>
        <?php endforeach; ?>
    </div>
</div>

<?php
// Only include styles once
if (!defined('SXL_HIGHLIGHTS_STYLES_LOADED')) :
    define('SXL_HIGHLIGHTS_STYLES_LOADED', true);
?>
<style>
/* Container */
.sxl-episode-highlights {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border-left: 4px solid #c2002f;
    margin-bottom: 24px;
}

/* Header */
.sxl-highlights-header {
    font-size: 18px;
    font-weight: 700;
    color: #004877;
    margin: 0 0 16px 0;
    padding-bottom: 12px;
    border-bottom: 2px solid #e9ecef;
    display: flex;
    align-items: center;
    gap: 8px;
}

.sxl-icon {
    font-size: 20px;
}

/* Wrapper */
.sxl-highlights-wrapper {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* Individual highlight item */
.sxl-highlight-item {
    display: flex;
    flex-direction: column;
    padding: 12px 14px;
    border-radius: 8px;
    text-decoration: none !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: #ffffff;
    border: 1px solid #e9ecef;
    cursor: pointer;
}

.sxl-highlight-item:hover {
    background: linear-gradient(135deg, #fff5f7 0%, #ffffff 100%);
    border-color: #c2002f;
    transform: translateX(6px);
    box-shadow: 0 4px 12px rgba(194, 0, 47, 0.15);
}

/* Timestamp */
.sxl-time {
    color: #c2002f;
    font-weight: 700;
    font-size: 13px;
    font-family: 'Monaco', 'Consolas', monospace;
    margin-bottom: 4px;
}

/* Topic description */
.sxl-topic {
    color: #333;
    font-size: 14px;
    line-height: 1.5;
    font-weight: 500;
}

.sxl-highlight-item:hover .sxl-topic {
    color: #c2002f;
}

/* Active/Playing state */
.sxl-highlight-item.is-playing {
    background: linear-gradient(135deg, #c2002f 0%, #a50028 100%);
    border-color: #c2002f;
}

.sxl-highlight-item.is-playing .sxl-time,
.sxl-highlight-item.is-playing .sxl-topic {
    color: #ffffff;
}

/* Responsive */
@media (max-width: 768px) {
    .sxl-episode-highlights {
        padding: 18px;
        margin: 16px 0;
    }
    
    .sxl-highlight-item {
        padding: 10px 12px;
    }
    
    .sxl-topic {
        font-size: 13px;
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const highlights = document.querySelectorAll('.sxl-highlight-item');
    
    highlights.forEach(function(highlight) {
        highlight.addEventListener('click', function(e) {
            e.preventDefault();
            
            const timeSeconds = parseInt(this.dataset.time);
            const episodeId = this.dataset.episode;
            const iframe = document.querySelector('iframe[src*="transistor.fm"]');
            
            if (iframe) {
                iframe.src = `https://share.transistor.fm/e/${episodeId}?time=${timeSeconds}`;
                iframe.scrollIntoView({ behavior: 'smooth', block: 'center' });
                highlights.forEach(h => h.classList.remove('is-playing'));
                this.classList.add('is-playing');
            } else {
                window.open(`https://share.transistor.fm/e/${episodeId}?time=${timeSeconds}`, '_blank');
            }
        });
    });
});
</script>
<?php endif; ?>
```

---

## Step 5: Create a Shortcode (Alternative to Template Part)

Add this to your child theme's `functions.php`:

```php
<?php
/**
 * Shortcode: Podcast Episode Highlights
 * Usage: [podcast_highlights]
 */
function sxl_podcast_highlights_shortcode($atts) {
    // Start output buffering
    ob_start();
    
    // Get the ACF fields
    $episode_id = get_field('transistor_episode_id');
    $highlights = get_field('episode_highlights');
    
    // Only display if we have data
    if (!$episode_id || !$highlights) {
        return '<p class="sxl-no-highlights">No episode highlights available.</p>';
    }
    ?>
    
    <div class="sxl-episode-highlights" data-episode-id="<?php echo esc_attr($episode_id); ?>">
        <h3 class="sxl-highlights-header">
            <span class="sxl-icon">🎙️</span> Episode Highlights
        </h3>
        
        <div class="sxl-highlights-wrapper">
            <?php foreach ($highlights as $highlight) : ?>
                <a href="#" 
                   class="sxl-highlight-item" 
                   data-time="<?php echo esc_attr($highlight['timestamp_seconds']); ?>" 
                   data-episode="<?php echo esc_attr($episode_id); ?>">
                    <span class="sxl-time">(<?php echo esc_html($highlight['timestamp_display']); ?>)</span>
                    <span class="sxl-topic"><?php echo esc_html($highlight['highlight_title']); ?></span>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
    
    <?php
    // Return the buffered content
    return ob_get_clean();
}
add_shortcode('podcast_highlights', 'sxl_podcast_highlights_shortcode');

/**
 * Enqueue Podcast Highlights Styles and Scripts
 */
function sxl_podcast_highlights_assets() {
    if (is_single() && has_shortcode(get_the_content(), 'podcast_highlights')) {
        wp_enqueue_style('sxl-podcast-highlights', get_stylesheet_directory_uri() . '/css/podcast-highlights.css', array(), '1.0.0');
        wp_enqueue_script('sxl-podcast-highlights', get_stylesheet_directory_uri() . '/js/podcast-highlights.js', array(), '1.0.0', true);
    }
}
add_action('wp_enqueue_scripts', 'sxl_podcast_highlights_assets');
```

---

## Step 6: Add CSS File (Optional - for cleaner code)

Create: `child-theme/css/podcast-highlights.css`

```css
/* Podcast Episode Highlights Styles */
/* (Copy all the CSS from the previous examples here) */
```

---

## Step 7: Add JavaScript File (Optional - for cleaner code)

Create: `child-theme/js/podcast-highlights.js`

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const highlights = document.querySelectorAll('.sxl-highlight-item');
    
    if (!highlights.length) return;
    
    highlights.forEach(function(highlight) {
        highlight.addEventListener('click', function(e) {
            e.preventDefault();
            
            const timeSeconds = parseInt(this.dataset.time);
            const episodeId = this.dataset.episode;
            const iframe = document.querySelector('iframe[src*="transistor.fm"]');
            
            if (iframe) {
                // Update iframe source to jump to timestamp
                iframe.src = `https://share.transistor.fm/e/${episodeId}?time=${timeSeconds}`;
                
                // Smooth scroll to player
                iframe.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
                
                // Visual feedback
                highlights.forEach(h => h.classList.remove('is-playing'));
                this.classList.add('is-playing');
                
            } else {
                // Fallback: open in new tab
                window.open(`https://share.transistor.fm/e/${episodeId}?time=${timeSeconds}`, '_blank');
            }
        });
    });
    
    // Optional: Auto-calculate seconds from MM:SS format
    function timeToSeconds(timeString) {
        const parts = timeString.split(':').map(Number);
        if (parts.length === 2) {
            return (parts[0] * 60) + parts[1];
        } else if (parts.length === 3) {
            return (parts[0] * 3600) + (parts[1] * 60) + parts[2];
        }
        return 0;
    }
});
```

---

## Step 8: Using the Shortcode in Elementor

1. Edit your podcast episode page in Elementor
2. Drag a **Shortcode** widget to your sidebar
3. Enter: `[podcast_highlights]`
4. Save and preview

---

## Step 9: Content Team Workflow

For each new podcast episode:

1. **Create/Edit the post** in WordPress
2. **Scroll down** to the "Podcast Episode Highlights" section
3. **Enter the Transistor Episode ID** (found in your Transistor dashboard)
4. **Click "Add Row"** for each highlight
5. **Enter:**
   - Timestamp Display: `05:42`
   - Timestamp Seconds: `342`
   - Highlight Title: `Personalization in sales with AI`
6. **Publish** the post

The highlights will automatically appear in the sidebar!

---

## Finding Your Transistor Episode ID

1. Log into your **Transistor.fm dashboard**
2. Go to your podcast → **Episodes**
3. Click on the episode
4. Look at the URL or the embed code
5. The Episode ID is the alphanumeric string after `/e/`
   - Example: `https://share.transistor.fm/e/5d8a4233` → ID is `5d8a4233`

---

## Quick Time Conversion Tool

Add this to your WordPress admin or use a quick converter:

```javascript
// Quick converter - paste in browser console or create a tool
function convertTime(mmss) {
    const [min, sec] = mmss.split(':').map(Number);
    return (min * 60) + sec;
}

// Examples:
console.log(convertTime('01:51')); // 111
console.log(convertTime('05:42')); // 342
console.log(convertTime('28:01')); // 1681
```

---

## Summary Comparison

| Feature | Option 1: HTML Snippet | Option 2: ACF Dynamic |
|---------|----------------------|----------------------|
| Setup Time | 5 minutes | 30-60 minutes |
| Per-Episode Effort | Edit HTML each time | Fill in form fields |
| Best For | Quick testing, few episodes | Ongoing podcast series |
| Technical Skill | Copy/paste | Basic WordPress knowledge |
| Scalability | Low | High |
| Content Team Friendly | No | Yes |

---

## Need Help?

If you encounter any issues:
1. Check that the Transistor iframe exists on the page
2. Verify the Episode ID is correct
3. Test the timestamp URL directly: `https://share.transistor.fm/e/[EPISODE_ID]?time=[SECONDS]`
4. Check browser console for JavaScript errors

---

*Document prepared by Rocket Clicks - January 2026*
