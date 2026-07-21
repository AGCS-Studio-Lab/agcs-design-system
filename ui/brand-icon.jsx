/**
 * The brand icon — the only "logo" in the system (a folder / forward-arrow
 * glyph). Not a wordmark. Lime on Obsidian/Paper covers; white for
 * lime-saturated grounds; black where lime is reserved elsewhere on Paper.
 *
 * Vendored file — canonical source: agcs-design-system/ui/brand-icon.jsx.
 * Assets: copy agcs-design-system/assets/agcs_lab_icon_{lime,black,white}.svg
 * into the host app's public/brand/. (Next apps may swap <img> for next/image.)
 */
import { cn } from "@/lib/utils";

const SRC = {
  lime: "/brand/agcs_lab_icon_lime.svg",
  black: "/brand/agcs_lab_icon_black.svg",
  white: "/brand/agcs_lab_icon_white.svg",
};

export function BrandIcon({ variant = "lime", size = 32, className, alt = "AGCS" }) {
  return (
    <img
      src={SRC[variant]}
      alt={alt}
      width={size}
      height={size}
      aria-hidden={alt === "" ? true : undefined}
      className={cn("block", className)}
    />
  );
}
