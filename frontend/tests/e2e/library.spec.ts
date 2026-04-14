import path from "path";

import { expect, test } from "@playwright/test";

test("upload, classify, and filter a library item", async ({ page }) => {
  const fixturePath = path.resolve(__dirname, "../fixtures/linen-shirt-test.svg");
  const uniqueName = `Playwright Designer ${Date.now()}`;

  await page.goto("/");

  await page.setInputFiles("#file-upload", fixturePath);
  await page.getByLabel("Designer").fill(uniqueName);
  await page.getByRole("button", { name: "Upload and classify" }).click();

  await expect(page.getByText("Upload complete. Placeholder AI metadata has been added.")).toBeVisible();
  await expect(page.getByRole("heading", { name: "linen shirt test" }).first()).toBeVisible();
  await expect(page.getByText("linen-shirt-test.svg").first()).toBeVisible();
  await expect(page.getByText("top").first()).toBeVisible();

  await page.getByLabel("Search library").fill("linen");
  await page.getByRole("button", { name: "Search" }).click();

  await expect(page.getByRole("heading", { name: "linen shirt test" }).first()).toBeVisible();
  await expect(page.getByText(uniqueName).first()).toBeVisible();
});
