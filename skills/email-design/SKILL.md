---
name: email-design
description: >
  HTML email template design with cross-client compatibility and responsive patterns.
  Trigger: user asks to "design an email", "build an email template", "create a newsletter",
  "HTML email", "email layout", "transactional email", "welcome email",
  "promotional email", or any email template work.
license: MIT
---

# Email Design

## Pre-Flight: Check Design Context

Before generating email template code:
1. Use `get_design_context` to check for existing brand colors, logos, fonts, or email design systems.
2. If a Figma URL is provided, pull screenshots and metadata to match the design.
3. Determine: What type of email? (welcome, newsletter, promotional, transactional) What ESP?

---

## 1. Fundamental Constraints

Email HTML is not web HTML. These constraints are non-negotiable:

| Rule | Why |
|------|-----|
| **Table-based layout** | Outlook and older clients don't support flexbox/grid |
| **Inline CSS** | Many clients strip `<style>` blocks |
| **No JavaScript** | Stripped by all email clients |
| **No external CSS** | Some clients block external resources |
| **Max width 600px** | Standard email client viewport |
| **Web-safe fonts** | Custom fonts require fallbacks |
| **Alt text on all images** | Images are often blocked by default |
| **No CSS variables** | Not supported in most email clients |
| **No shorthand properties** | Use `padding-top`, not `padding: 10px` in some clients |

---

## 2. Base Email Structure

```html
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="color-scheme" content="light dark" />
  <meta name="supported-color-schemes" content="light dark" />
  <title>Email Subject Line</title>

  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->

  <style>
    /* Reset styles */
    body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
    img { -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%;
      outline: none; text-decoration: none; }
    body { margin: 0; padding: 0; width: 100% !important; height: 100% !important; }

    /* Responsive styles */
    @media only screen and (max-width: 620px) {
      .email-container { width: 100% !important; max-width: 100% !important; }
      .fluid { max-width: 100% !important; height: auto !important; }
      .stack-column { display: block !important; width: 100% !important; }
      .stack-column-center { text-align: center !important; }
      .center-on-narrow { text-align: center !important; display: block !important;
        margin-left: auto !important; margin-right: auto !important; float: none !important; }
      table.center-on-narrow { display: inline-block !important; }
      .hide-on-mobile { display: none !important; }
      .padding-mobile { padding: 20px !important; }
    }

    /* Dark mode */
    @media (prefers-color-scheme: dark) {
      .email-bg { background-color: #1a1a2e !important; }
      .dark-bg { background-color: #16213e !important; }
      .dark-text { color: #e0e0e0 !important; }
      .dark-text-secondary { color: #a0a0a0 !important; }
      h1, h2, h3 { color: #ffffff !important; }
    }
    [data-ogsc] .dark-bg { background-color: #16213e !important; }
    [data-ogsc] .dark-text { color: #e0e0e0 !important; }
  </style>
</head>

<body style="margin: 0; padding: 0; background-color: #f4f4f7; font-family: -apple-system,
  BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;"
  class="email-bg">

  <!-- Preview text (hidden) -->
  <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0;
    max-width: 0; opacity: 0; overflow: hidden;">
    Your preview text goes here. Keep it under 100 characters.
    &#847; &#847; &#847; <!-- Prevent client from pulling in other text -->
  </div>

  <!-- Outer table for full-width background -->
  <table role="presentation" cellpadding="0" cellspacing="0" border="0"
    width="100%" style="background-color: #f4f4f7;" class="email-bg">
    <tr>
      <td align="center" style="padding: 20px 0;">

        <!-- Email container: 600px max -->
        <table role="presentation" cellpadding="0" cellspacing="0" border="0"
          width="600" class="email-container"
          style="max-width: 600px; width: 100%; background-color: #ffffff; border-radius: 8px;
            overflow: hidden;" class="dark-bg">

          <!-- HEADER -->
          <!-- HERO -->
          <!-- CONTENT -->
          <!-- CTA -->
          <!-- FOOTER -->

        </table>

      </td>
    </tr>
  </table>
</body>
</html>
```

---

## 3. MSO Conditional Comments (Outlook)

Outlook uses Word as its rendering engine. Use MSO conditionals for Outlook-specific fixes.

```html
<!-- Target Outlook only -->
<!--[if mso]>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600">
    <tr><td>
<![endif]-->

  <!-- Your fluid content here -->

<!--[if mso]>
    </td></tr>
  </table>
<![endif]-->
```

Common MSO fixes: force `border-collapse: collapse` and explicit widths in `[if mso]` style blocks. For Outlook rounded buttons, use VML `<v:roundrect>` with `arcsize`, `fillcolor`, and `<center>` for text, wrapped in `[if mso]` / `[if !mso]` conditionals with a standard `<a>` fallback.

---

## 4. Responsive Email (Fluid Hybrid Method)

The fluid hybrid approach works without media queries in clients that don't support them.

### Two-Column Layout
```html
<!--[if mso]>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600">
  <tr><td width="290" valign="top"><![endif]-->

<div style="display: inline-block; width: 100%; max-width: 290px; vertical-align: top;"
  class="stack-column">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td style="padding: 20px;">
        <h2 style="margin: 0; font-size: 20px; color: #1a1a2e;">Column 1</h2>
        <p style="margin: 12px 0 0; font-size: 15px; line-height: 1.5; color: #555;">
          Content for the first column.
        </p>
      </td>
    </tr>
  </table>
</div>

<!--[if mso]></td><td width="290" valign="top"><![endif]-->

<div style="display: inline-block; width: 100%; max-width: 290px; vertical-align: top;"
  class="stack-column">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td style="padding: 20px;">
        <h2 style="margin: 0; font-size: 20px; color: #1a1a2e;">Column 2</h2>
        <p style="margin: 12px 0 0; font-size: 15px; line-height: 1.5; color: #555;">
          Content for the second column.
        </p>
      </td>
    </tr>
  </table>
</div>

<!--[if mso]></td></tr></table><![endif]-->
```

---

## 5. Email Typography

### Web-Safe Font Stacks
```css
/* Sans-serif (most common) */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;

/* Serif */
font-family: Georgia, 'Times New Roman', Times, serif;

/* Monospace (for code) */
font-family: 'Courier New', Courier, monospace;
```

### Web Font Loading (Limited Support)
```html
<!-- Works in Apple Mail, iOS Mail, Android default, Thunderbird -->
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
</style>
```

### Typography Scale for Email
| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 (hero) | 28–32px | 700 | 1.2 |
| H2 (section) | 22–24px | 700 | 1.25 |
| H3 (subsection) | 18–20px | 600 | 1.3 |
| Body | 15–16px | 400 | 1.5 |
| Small / Caption | 13px | 400 | 1.4 |

### Rules
- Minimum body font size: 14px (some clients enforce this).
- Use `px` not `rem` or `em` in emails.
- Set `line-height` as a multiplier, not in px.
- Always specify `color` inline on text elements.

---

## 6. Bulletproof Buttons

Buttons that work in every email client, including Outlook.

### Method: Padding-Based (Best)
```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="border-radius: 8px; background-color: #4F46E5;" class="button-bg">
      <a href="https://example.com" target="_blank"
        style="display: inline-block; padding: 14px 32px; font-size: 16px;
          font-weight: 600; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
          Roboto, sans-serif; color: #ffffff; text-decoration: none;
          border-radius: 8px;">
        Get Started Free
      </a>
    </td>
  </tr>
</table>
```

### Button Rules
- Minimum size: 44px tall, 150px+ wide.
- Use `display: inline-block` with padding (not fixed width).
- Add `target="_blank"` on all links.
- Set both `background-color` on the `<td>` AND the `<a>` for Outlook.
- `border-radius` on `<td>` works in most clients but not Outlook.
- For Outlook rounded buttons, use VML (see section 3).

---

## 7. Email Section Templates

### Header
```html
<tr>
  <td style="padding: 24px 32px; text-align: center;">
    <img src="https://example.com/logo.png" alt="Company Name"
      width="120" style="display: block; margin: 0 auto;" />
  </td>
</tr>
```

### Hero Section
```html
<tr>
  <td style="padding: 40px 32px; text-align: center; background-color: #4F46E5;"
    class="padding-mobile">
    <h1 style="margin: 0; font-size: 30px; font-weight: 700; color: #ffffff;
      line-height: 1.2;">
      Welcome to Our Platform
    </h1>
    <p style="margin: 16px 0 0; font-size: 16px; color: rgba(255,255,255,0.8);
      line-height: 1.5;">
      You're all set to start building amazing things.
    </p>
    <!-- CTA button here -->
  </td>
</tr>
```

### Content Block
```html
<tr>
  <td style="padding: 32px;" class="padding-mobile">
    <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #1a1a2e;
      line-height: 1.25;" class="dark-text">
      What's inside
    </h2>
    <p style="margin: 12px 0 0; font-size: 15px; line-height: 1.6; color: #555;"
      class="dark-text-secondary">
      Here's what you can do to get started with your account.
    </p>
  </td>
</tr>
```

### Feature Row (Icon + Text)
```html
<tr>
  <td style="padding: 0 32px 24px;" class="padding-mobile">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td width="48" valign="top" style="padding-right: 16px;">
          <img src="https://example.com/icon-check.png" alt="" width="40" height="40"
            style="display: block;" />
        </td>
        <td valign="top">
          <h3 style="margin: 0; font-size: 16px; font-weight: 600; color: #1a1a2e;">
            Quick Setup
          </h3>
          <p style="margin: 4px 0 0; font-size: 14px; line-height: 1.5; color: #666;">
            Get up and running in less than 5 minutes.
          </p>
        </td>
      </tr>
    </table>
  </td>
</tr>
```

### Footer
```html
<tr>
  <td style="padding: 24px 32px; text-align: center; border-top: 1px solid #e5e7eb;">
    <!-- Social icons -->
    <table role="presentation" cellpadding="0" cellspacing="0" border="0"
      style="margin: 0 auto;">
      <tr>
        <td style="padding: 0 8px;">
          <a href="#"><img src="https://example.com/icon-twitter.png" alt="Twitter"
            width="24" height="24" /></a>
        </td>
        <td style="padding: 0 8px;">
          <a href="#"><img src="https://example.com/icon-linkedin.png" alt="LinkedIn"
            width="24" height="24" /></a>
        </td>
      </tr>
    </table>
    <!-- Company info -->
    <p style="margin: 16px 0 0; font-size: 13px; line-height: 1.5; color: #999;">
      Company Name, 123 Street, City, State 12345<br />
      <a href="#" style="color: #999; text-decoration: underline;">Unsubscribe</a>
      &nbsp;|&nbsp;
      <a href="#" style="color: #999; text-decoration: underline;">Manage preferences</a>
    </p>
  </td>
</tr>
```

---

## 8. Dark Mode Email Considerations

### Meta Tags (Required)
```html
<meta name="color-scheme" content="light dark" />
<meta name="supported-color-schemes" content="light dark" />
```

### CSS Targeting
```css
/* Apple Mail, iOS Mail */
@media (prefers-color-scheme: dark) {
  .email-bg { background-color: #1a1a2e !important; }
  .dark-bg { background-color: #16213e !important; }
  .dark-text { color: #e0e0e0 !important; }
}

/* Outlook.com */
[data-ogsc] .dark-bg { background-color: #16213e !important; }
[data-ogsc] .dark-text { color: #e0e0e0 !important; }
```

### Image Handling
- Use transparent PNGs where possible (adapt to any background).
- Add a white outline/glow to dark logos so they're visible on dark backgrounds.
- Test with images blocked — alt text should convey the message.

---

## 9. Image Optimization

### Rules
| Guideline | Value |
|-----------|-------|
| Max file size per image | 200KB |
| Total email size | Under 100KB HTML + 800KB images |
| Format | PNG for graphics, JPEG for photos |
| Retina | Serve 2x, set `width` attribute to 1x |
| Alt text | Always. Styled alt text as fallback. |

### Retina Images
```html
<!-- Image is 600px wide visually, but served at 1200px for retina -->
<img src="https://example.com/hero-1200.jpg" alt="Product showcase"
  width="600" style="display: block; width: 100%; max-width: 600px; height: auto;" />
```

### Styled Alt Text
```html
<img src="https://example.com/hero.jpg"
  alt="Spring Sale: 40% off everything"
  width="600"
  style="display: block; width: 100%; max-width: 600px; height: auto;
    font-family: sans-serif; font-size: 24px; font-weight: bold;
    color: #4F46E5; background-color: #EEF2FF; text-align: center; padding: 40px;" />
```

---

## 10. Template Types

### Welcome Email
- Hero with brand color background
- Personalized greeting ("Hi {first_name}")
- 3 quick-start steps with icons
- Primary CTA: "Get started" or "Complete your profile"
- Optional: onboarding video thumbnail

### Newsletter
- Simple header with logo + date
- Featured article with large image
- 2-column article grid below
- Short excerpts (2–3 lines) with "Read more" links
- Footer with social links and unsubscribe

### Promotional
- Bold hero with offer ("40% OFF")
- Product grid (2 columns)
- Each product: image, name, price, CTA
- Urgency: "Ends Sunday" or countdown
- Trust signals: free shipping, returns

### Transactional
- Minimal design, clear information
- Order confirmation: items, quantities, prices, total
- Shipping update: tracking number, delivery date
- Password reset: single CTA button, security note
- No promotional content (improves deliverability)

---

## Email Design Checklist

- [ ] Table-based layout (no flexbox/grid)
- [ ] All critical styles are inline
- [ ] Max width 600px
- [ ] All images have alt text and width/height attributes
- [ ] Bulletproof buttons (padding-based or VML)
- [ ] MSO conditionals for Outlook
- [ ] Responsive at 320px–600px (fluid hybrid)
- [ ] Web-safe fonts with fallback stack
- [ ] Preview text is set (hidden preheader)
- [ ] Dark mode meta tags and CSS included
- [ ] Images under 200KB each, total email under 100KB HTML
- [ ] Unsubscribe link in footer
- [ ] Tested in Litmus or Email on Acid across major clients
- [ ] Links have `target="_blank"`
- [ ] `role="presentation"` on all layout tables
