# Sales Xceleration Episode Highlights
## ACF Integration Update Guide

**Based on:** Existing "Podcast Fields" ACF Field Group  
**Current Field:** `episode_highlights` (WYSIWYG Editor)  
**Goal:** Make highlights clickable with Transistor.fm timestamp navigation

---

## Current Setup Analysis

Your existing ACF Field Group "Podcast Fields" already includes:
- ✅ `episode_highlights` field (#7) - Currently a WYSIWYG Editor
- ✅ `schema_embed_url` field (#6) - Contains the Transistor embed URL
- ✅ `key_takeaways` field (#8) - Already uses Repeater format

---

## Two Implementation Options

### Option A: Quick Fix - Parse Existing WYSIWYG Content
**Effort:** Low (No ACF changes needed)  
**Best for:** Immediate implementation

### Option B: Convert to Repeater Field  
**Effort:** Medium (Requires ACF field update)  
**Best for:** Long-term scalability, cleaner data

---

# Option A: Quick Fix - Parse WYSIWYG Content

Keep the existing WYSIWYG field and enter timestamps in a structured format.

## Step 1: Content Entry Format

When editing a podcast post, enter highlights in the WYSIWYG like this:

```
(00:00) Intro
(01:51) AI tools for SMBs and how to implement them
(05:42) Personalization in sales with AI
(07:57) Smarter targeting starts with human insight
(11:35) Balancing quantity and quality in lead gen
(20:06) Hyper-personalization strategies
(28:01) Where AI can take sales in the future
```

Each line should start with `(MM:SS)` followed by the topic.

## Step 2: Add This PHP/Shortcode to functions.php

```php
<?php
/**
 * Podcast Episode Highlights Shortcode
 * Parses WYSIWYG content and creates clickable timestamp links
 * Usage: [podcast_highlights_parsed]
 */
function sxl_podcast_highlights_parsed_shortcode() {
    // Get the fields
    $highlights_content = get_field('episode_highlights');
    $embed_url = get_field('schema_embed_url');
    
    if (!$highlights_content) {
        return '';
    }
    
    // Extract episode ID from embed URL
    // Format: https://share.transistor.fm/e/5d8a4233
    $episode_id = '';
    if ($embed_url && preg_match('/transistor\.fm\/e\/([a-zA-Z0-9]+)/', $embed_url, $matches)) {
        $episode_id = $matches[1];
    }
    
    if (!$episode_id) {
        // Try to get from player_embed_code as fallback
        $embed_code = get_field('player_embed_code');
        if ($embed_code && preg_match('/transistor\.fm\/e\/([a-zA-Z0-9]+)/', $embed_code, $matches)) {
            $episode_id = $matches[1];
        }
    }
    
    // Parse the highlights content
    // Look for pattern: (MM:SS) Description
    $lines = preg_split('/\r\n|\r|\n/', strip_tags($highlights_content));
    $parsed_highlights = array();
    
    foreach ($lines as $line) {
        $line = trim($line);
        if (empty($line)) continue;
        
        // Match (MM:SS) or (HH:MM:SS) format
        if (preg_match('/^\((\d{1,2}:\d{2}(?::\d{2})?)\)\s*(.+)$/', $line, $matches)) {
            $timestamp_display = $matches[1];
            $topic = trim($matches[2]);
            
            // Convert to seconds
            $parts = explode(':', $timestamp_display);
            if (count($parts) == 2) {
                $seconds = (intval($parts[0]) * 60) + intval($parts[1]);
            } else if (count($parts) == 3) {
                $seconds = (intval($parts[0]) * 3600) + (intval($parts[1]) * 60) + intval($parts[2]);
            } else {
                $seconds = 0;
            }
            
            $parsed_highlights[] = array(
                'display' => $timestamp_display,
                'seconds' => $seconds,
                'topic' => $topic
            );
        }
    }
    
    if (empty($parsed_highlights)) {
        return '';
    }
    
    // Generate output
    ob_start();
    ?>
    <div class="sxl-episode-highlights" data-episode-id="<?php echo esc_attr($episode_id); ?>">
        <h3 class="sxl-highlights-header">
            <span class="sxl-icon">🎙️</span> Episode Highlights
        </h3>
        
        <div class="sxl-highlights-wrapper">
            <?php foreach ($parsed_highlights as $highlight) : ?>
                <a href="#" 
                   class="sxl-highlight-item" 
                   data-time="<?php echo esc_attr($highlight['seconds']); ?>" 
                   data-episode="<?php echo esc_attr($episode_id); ?>">
                    <span class="sxl-time">(<?php echo esc_html($highlight['display']); ?>)</span>
                    <span class="sxl-topic"><?php echo esc_html($highlight['topic']); ?></span>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
    
    <style>
    .sxl-episode-highlights {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #c2002f;
        margin-bottom: 24px;
    }
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
    .sxl-icon { font-size: 20px; }
    .sxl-highlights-wrapper {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
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
    .sxl-time {
        color: #c2002f;
        font-weight: 700;
        font-size: 13px;
        font-family: 'Monaco', 'Consolas', monospace;
        margin-bottom: 4px;
    }
    .sxl-topic {
        color: #333;
        font-size: 14px;
        line-height: 1.5;
        font-weight: 500;
    }
    .sxl-highlight-item:hover .sxl-topic { color: #c2002f; }
    .sxl-highlight-item.is-playing {
        background: linear-gradient(135deg, #c2002f 0%, #a50028 100%);
        border-color: #c2002f;
    }
    .sxl-highlight-item.is-playing .sxl-time,
    .sxl-highlight-item.is-playing .sxl-topic { color: #ffffff; }
    @media (max-width: 768px) {
        .sxl-episode-highlights { padding: 18px; margin: 16px 0; }
        .sxl-highlight-item { padding: 10px 12px; }
        .sxl-topic { font-size: 13px; }
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
                    iframe.src = 'https://share.transistor.fm/e/' + episodeId + '?time=' + timeSeconds;
                    iframe.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    highlights.forEach(function(h) { h.classList.remove('is-playing'); });
                    this.classList.add('is-playing');
                } else {
                    window.open('https://share.transistor.fm/e/' + episodeId + '?time=' + timeSeconds, '_blank');
                }
            });
        });
    });
    </script>
    <?php
    return ob_get_clean();
}
add_shortcode('podcast_highlights_parsed', 'sxl_podcast_highlights_parsed_shortcode');
```

## Step 3: Use in Elementor

In your sidebar, add a **Shortcode widget** with:
```
[podcast_highlights_parsed]
```

## Step 4: Content Entry Example

In the WYSIWYG "Episode Highlights" field, enter:

```
(00:00) Intro - Welcome and guest introduction
(01:51) AI tools for SMBs and how to implement them
(05:42) Personalization in sales with AI
(07:57) Smarter targeting starts with human insight
(11:35) Balancing quantity and quality in lead gen
(20:06) Hyper-personalization strategies
(28:01) Where AI can take sales in the future
(33:03) Closing thoughts and resources
```

The shortcode will automatically:
1. Parse each line
2. Extract the timestamp
3. Convert MM:SS to seconds
4. Extract the episode ID from `schema_embed_url`
5. Generate clickable links

---

# Option B: Convert to Repeater Field (Recommended)

This provides cleaner data entry and validation.

## Step 1: Modify the ACF Field

1. Go to **ACF** → **Field Groups** → **Podcast Fields**
2. Find field #7 "Episode Highlights" (`episode_highlights`)
3. Click **Edit** on this field
4. Change the field type from **WYSIWYG Editor** to **Repeater**

## Step 2: Add Sub-Fields to the Repeater

Configure the repeater with these sub-fields:

### Sub-field 1: Timestamp Display
| Setting | Value |
|---------|-------|
| Label | Timestamp |
| Name | `highlight_timestamp` |
| Type | Text |
| Placeholder | 00:00 |
| Instructions | Enter in MM:SS format |
| Max Length | 8 |

### Sub-field 2: Timestamp Seconds
| Setting | Value |
|---------|-------|
| Label | Seconds |
| Name | `highlight_seconds` |
| Type | Number |
| Instructions | Time in seconds. Formula: (Min × 60) + Sec |
| Minimum | 0 |

### Sub-field 3: Topic
| Setting | Value |
|---------|-------|
| Label | Topic |
| Name | `highlight_topic` |
| Type | Text |
| Instructions | Brief description of this segment |
| Max Length | 150 |

## Step 3: Repeater Settings

| Setting | Value |
|---------|-------|
| Layout | Table |
| Button Label | Add Highlight |
| Minimum Rows | 0 |
| Maximum Rows | 20 |

## Step 4: Update the Shortcode

Replace the previous shortcode with this updated version:

```php
<?php
/**
 * Podcast Episode Highlights Shortcode (Repeater Version)
 * Usage: [podcast_highlights]
 */
function sxl_podcast_highlights_shortcode() {
    // Get the episode highlights repeater
    $highlights = get_field('episode_highlights');
    $embed_url = get_field('schema_embed_url');
    
    if (!$highlights || !is_array($highlights)) {
        return '';
    }
    
    // Extract episode ID from embed URL
    $episode_id = '';
    if ($embed_url && preg_match('/transistor\.fm\/e\/([a-zA-Z0-9]+)/', $embed_url, $matches)) {
        $episode_id = $matches[1];
    }
    
    if (!$episode_id) {
        $embed_code = get_field('player_embed_code');
        if ($embed_code && preg_match('/transistor\.fm\/e\/([a-zA-Z0-9]+)/', $embed_code, $matches)) {
            $episode_id = $matches[1];
        }
    }
    
    ob_start();
    ?>
    <div class="sxl-episode-highlights" data-episode-id="<?php echo esc_attr($episode_id); ?>">
        <h3 class="sxl-highlights-header">
            <span class="sxl-icon">🎙️</span> Episode Highlights
        </h3>
        
        <div class="sxl-highlights-wrapper">
            <?php foreach ($highlights as $highlight) : 
                $timestamp = isset($highlight['highlight_timestamp']) ? $highlight['highlight_timestamp'] : '';
                $seconds = isset($highlight['highlight_seconds']) ? intval($highlight['highlight_seconds']) : 0;
                $topic = isset($highlight['highlight_topic']) ? $highlight['highlight_topic'] : '';
                
                if (empty($topic)) continue;
            ?>
                <a href="#" 
                   class="sxl-highlight-item" 
                   data-time="<?php echo esc_attr($seconds); ?>" 
                   data-episode="<?php echo esc_attr($episode_id); ?>">
                    <span class="sxl-time">(<?php echo esc_html($timestamp); ?>)</span>
                    <span class="sxl-topic"><?php echo esc_html($topic); ?></span>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
    
    <style>
    .sxl-episode-highlights {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #c2002f;
        margin-bottom: 24px;
    }
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
    .sxl-icon { font-size: 20px; }
    .sxl-highlights-wrapper {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
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
    .sxl-time {
        color: #c2002f;
        font-weight: 700;
        font-size: 13px;
        font-family: 'Monaco', 'Consolas', monospace;
        margin-bottom: 4px;
    }
    .sxl-topic {
        color: #333;
        font-size: 14px;
        line-height: 1.5;
        font-weight: 500;
    }
    .sxl-highlight-item:hover .sxl-topic { color: #c2002f; }
    .sxl-highlight-item.is-playing {
        background: linear-gradient(135deg, #c2002f 0%, #a50028 100%);
        border-color: #c2002f;
    }
    .sxl-highlight-item.is-playing .sxl-time,
    .sxl-highlight-item.is-playing .sxl-topic { color: #ffffff; }
    @media (max-width: 768px) {
        .sxl-episode-highlights { padding: 18px; margin: 16px 0; }
        .sxl-highlight-item { padding: 10px 12px; }
        .sxl-topic { font-size: 13px; }
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
                    iframe.src = 'https://share.transistor.fm/e/' + episodeId + '?time=' + timeSeconds;
                    iframe.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    highlights.forEach(function(h) { h.classList.remove('is-playing'); });
                    this.classList.add('is-playing');
                } else {
                    window.open('https://share.transistor.fm/e/' + episodeId + '?time=' + timeSeconds, '_blank');
                }
            });
        });
    });
    </script>
    <?php
    return ob_get_clean();
}
add_shortcode('podcast_highlights', 'sxl_podcast_highlights_shortcode');
```

## Step 5: Data Entry in WordPress

When editing a podcast post, the Episode Highlights field will now show:

| Timestamp | Seconds | Topic |
|-----------|---------|-------|
| 00:00 | 0 | Intro |
| 01:51 | 111 | AI tools for SMBs |
| 05:42 | 342 | Personalization in sales |
| ... | ... | ... |

Click **Add Highlight** to add more rows.

---

# Elementor Integration

## For Single Post Template

If using Elementor Theme Builder:

1. Edit your **Single Post Template** for podcasts
2. Add a **Shortcode widget** in the sidebar
3. Enter: `[podcast_highlights]` or `[podcast_highlights_parsed]`

## For Individual Posts

1. Edit the post in Elementor
2. Drag a **Shortcode widget** to the sidebar column
3. Enter: `[podcast_highlights]`

---

# Quick Reference: Time Conversion

Use this JavaScript function to quickly convert MM:SS to seconds:

```javascript
function toSeconds(time) {
    const [m, s] = time.split(':').map(Number);
    return (m * 60) + s;
}

// Examples:
toSeconds('01:51');  // Returns: 111
toSeconds('05:42');  // Returns: 342
toSeconds('28:01');  // Returns: 1681
```

Or use this table:

| MM:SS | Seconds |
|-------|---------|
| 00:00 | 0 |
| 01:00 | 60 |
| 01:51 | 111 |
| 05:00 | 300 |
| 05:42 | 342 |
| 10:00 | 600 |
| 15:00 | 900 |
| 20:06 | 1206 |
| 25:00 | 1500 |
| 28:01 | 1681 |
| 30:00 | 1800 |
| 33:03 | 1983 |

---

# Summary: Which Option to Choose?

| Consideration | Option A (WYSIWYG Parse) | Option B (Repeater) |
|---------------|-------------------------|---------------------|
| ACF Changes Required | None | Yes - modify field type |
| Data Migration | Keep existing content | May need to re-enter |
| Content Entry | Type in format `(MM:SS) Topic` | Fill in table fields |
| Validation | Manual | Built-in |
| Error Prone | Slightly (formatting) | Less |
| Team Onboarding | Need format documentation | Self-explanatory UI |

**Recommendation:** 
- Start with **Option A** for immediate implementation
- Migrate to **Option B** when ready for cleaner long-term management

---

*Document updated based on existing ACF "Podcast Fields" configuration*
*Prepared by Rocket Clicks - January 2026*
