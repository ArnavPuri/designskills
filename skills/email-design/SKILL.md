---
name: email-design
description: >
  Coded HTML email templates that render across Outlook, Gmail, Apple Mail, and mobile:
  table layout, fluid-hybrid responsiveness, bulletproof buttons, email dark mode, and size
  limits. Use when the user asks to "design an email", "build an email template", "create a
  newsletter", "HTML email", "email layout", "transactional email", "welcome email",
  "promotional email", or any email template work. Not for web landing pages
  (landing-page-design) or web dark themes (dark-mode).
license: MIT
---

# Email Design

## Before You Start: Load Design Context

1. **Read `.agents/design-context.md`** (written by the `design-context` skill). If it is missing, look for tokens in `tailwind.config.*` or `:root` CSS variables. If nothing exists, use the defaults (Primary `#2563EB`, Secondary `#7C3AED`, Accent `#F59E0B`, Tailwind gray neutrals, Inter for headings and body, Minimal style) and **tell the user defaults were used** — suggest running `design-context`.
2. **Inline the hex values** — email clients don't support CSS variables. Use Primary for buttons and links, Neutral 900/800/500 for headings, body and muted text, Neutral 50/100 for the outer background, and put the brand heading/body font first in each web-safe stack (section 5). The `#4F46E5`-style hex values below are placeholders.
3. **Figma:** if the user gives a Figma URL, pull it with the Figma MCP (`get_design_context`, `get_screenshot`) and match it; it overrides the context file for that design.
4. Ask: what type of email (welcome, newsletter, promotional, transactional) and which ESP (it may need its own merge tags and template syntax)?

---

## 1. Fundamental Constraints

Email HTML is not web HTML. These constraints are non-negotiable:

| Rule | Why |
|------|-----|
| **Table-based layout** | Outlook for Windows (Word rendering engine) has no flexbox, grid, `max-width`, or reliable `float` |
| **Inline CSS** | Some clients strip or partly ignore `<style>` (Gmail for non-Google accounts, many webmail/older clients); keep `<style>` only for media queries and dark mode |
| **No JavaScript** | Stripped by all email clients |
| **No external CSS** | Some clients block external resources |
| **Max width 600px** | Standard email client viewport (600–640px) |
| **HTML under ~100KB** | Gmail clips messages over 102KB — content, the unsubscribe link, and the open-tracking pixel get hidden behind "View entire message" |
| **Web-safe fonts** | Custom fonts require fallbacks |
| **Alt text on all images** | Images are often blocked by default |
| **No CSS variables** | Not supported in most email clients |
| **Padding on `<td>`, not `<a>`/`<p>`/`<div>`** | Outlook desktop ignores padding/margin on many elements, plus `border-radius`, background images (without VML), and `rgba()` colors |

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
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no" />
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
    :root { color-scheme: light dark; supported-color-schemes: light dark; }
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

    /* Dark mode: Apple Mail, iOS Mail, Outlook for Mac/iOS/Android, some others */
    @media (prefers-color-scheme: dark) {
      .email-bg { background-color: #121212 !important; }
      .dark-bg { background-color: #1e1e1e !important; }
      .dark-text { color: #e6e6e6 !important; }
      .dark-text-secondary { color: #b3b3b3 !important; }
      h1, h2, h3 { color: #f2f2f2 !important; }
    }
    /* Outlook.com / Outlook apps: [data-ogsb] = backgrounds, [data-ogsc] = text colors */
    [data-ogsb] .email-bg { background-color: #121212 !important; }
    [data-ogsb] .dark-bg { background-color: #1e1e1e !important; }
    [data-ogsc] .dark-text { color: #e6e6e6 !important; }
    [data-ogsc] .dark-text-secondary { color: #b3b3b3 !important; }
  </style>
</head>

<body style="margin: 0; padding: 0; background-color: #f4f4f7; font-family: -apple-system,
  BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;"
  class="email-bg">
  <div role="article" aria-roledescription="email" aria-label="Email Subject Line" lang="en">

  <!-- Preview text (hidden) -->
  <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0;
    max-width: 0; opacity: 0; overflow: hidden; mso-hide: all;">
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
          width="600" class="email-container dark-bg"
          style="max-width: 600px; width: 100%; background-color: #ffffff; border-radius: 8px;
            overflow: hidden;">

          <!-- HEADER -->
          <!-- HERO -->
          <!-- CONTENT -->
          <!-- CTA -->
          <!-- FOOTER -->

        </table>

      </td>
    </tr>
  </table>
  </div>
</body>
</html>
```

---

## 3. MSO Conditional Comments (Outlook)

Classic Outlook for Windows (2007–2021, 365 desktop) renders with Microsoft Word. The "new Outlook" for Windows and Outlook.com use a browser engine, but classic Outlook is still widely used — keep supporting it. Use MSO conditionals for Word-engine fixes.

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
Put the design-context font first, then a web-safe fallback stack:
- **Sans:** `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`
- **Serif:** `Georgia, 'Times New Roman', Times, serif` · **Mono:** `'Courier New', Courier, monospace`

### Web Font Loading (Limited Support)
Gmail and Outlook ignore web fonts. Classic Outlook falls back to Times New Roman when the first font isn't installed — add `<!--[if mso]><style>h1,h2,h3,p,td,a { font-family: Arial, sans-serif !important; }</style><![endif]-->`.
Where supported (Apple Mail, iOS Mail, Samsung Mail, Thunderbird), load it in `<head>`: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">`.

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
    <td style="border-radius: 8px; background-color: #4F46E5; mso-padding-alt: 14px 32px;"
      class="button-bg">
      <a href="https://example.com" target="_blank"
        style="display: inline-block; padding: 14px 32px; background-color: #4F46E5; font-size: 16px;
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
- Set `background-color` on both the `<td>` and the `<a>`; Outlook ignores the `<a>` padding, so `mso-padding-alt` on the `<td>` restores the button size there (only the text is clickable in Outlook).
- `border-radius` works in most clients but not classic Outlook (square corners there).
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
    <!-- Solid hex, not rgba(): classic Outlook doesn't support rgba -->
    <p style="margin: 16px 0 0; font-size: 16px; color: #E0E7FF;
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
    <!-- #6b6b6b, not #999: footer text still needs 4.5:1 on white -->
    <p style="margin: 16px 0 0; font-size: 13px; line-height: 1.5; color: #6b6b6b;">
      Company Name, 123 Street, City, State 12345<br />
      <a href="#" style="color: #6b6b6b; text-decoration: underline;">Unsubscribe</a>
      &nbsp;|&nbsp;
      <a href="#" style="color: #6b6b6b; text-decoration: underline;">Manage preferences</a>
    </p>
  </td>
</tr>
```

---

## 8. Dark Mode Email Considerations

The base structure (section 2) already includes the required pieces: the `color-scheme` / `supported-color-schemes` meta tags and `:root` rule, a `prefers-color-scheme: dark` block, and `[data-ogsb]` / `[data-ogsc]` overrides for Outlook.com and the Outlook apps.

### How Clients Behave
| Client | Behavior | What you control |
|--------|----------|------------------|
| Apple Mail, iOS Mail, Outlook Mac | Honor `prefers-color-scheme` | Full custom dark palette |
| Outlook.com, Outlook iOS/Android | Partial auto-invert | `[data-ogsb]` / `[data-ogsc]` overrides |
| Gmail app (iOS/Android) | Full or partial forced inversion | Nothing — design to survive it |

- Avoid pure `#000`/`#fff` pairs; mid-dark backgrounds (`#121212`–`#1e1e1e`) with off-white text invert more gracefully.
- Keep brand colors on buttons as `background-color` on the `<td>` so inversion doesn't turn text unreadable.

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
| Total email size | HTML under 102KB (Gmail clipping; aim for < 80KB) + under ~1MB of images |
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

### Deliverability Basics (All Types)
- Bulk senders (Gmail/Yahoo rules since 2024): one-click unsubscribe headers (`List-Unsubscribe` + `List-Unsubscribe-Post`, RFC 8058), SPF/DKIM/DMARC, and a visible unsubscribe link.
- Always include a plain-text alternative part and a physical mailing address in the footer.

---

## Verify: Render and Check

Don't hand over an email you haven't looked at. After generating it:
1. Screenshot it in a browser at 390px and 1440px, e.g. `npx playwright screenshot --full-page --viewport-size=390,844 file://$PWD/email.html mobile.png`. The desktop shot should show a centered 600px column; the mobile shot should stack columns with no horizontal scroll.
2. Take a dark screenshot (`--color-scheme=dark`) and an images-off pass (remove `src` attributes) — the message and CTA must still read.
3. Check the file size: `wc -c email.html` must be under ~100KB after inlining.
4. For real client coverage (classic Outlook, Gmail app), send through Litmus / Email on Acid or a test inbox — a browser can't emulate the Word engine. Tell the user this step is still needed if you can't run it.

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
- [ ] Images under 200KB each; HTML under 102KB so Gmail doesn't clip it
- [ ] Tested in Litmus or Email on Acid across major clients
- [ ] Unsubscribe + physical address in footer; `List-Unsubscribe` headers set in the ESP
- [ ] Rendered and screenshotted at 390px and 1440px, light and dark (see Verify)
- [ ] `role="presentation"` on all layout tables
